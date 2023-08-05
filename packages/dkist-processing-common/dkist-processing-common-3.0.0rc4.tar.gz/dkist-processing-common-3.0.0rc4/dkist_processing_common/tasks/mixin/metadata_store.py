"""Mixin for a WorkflowDataTaskBase subclass which implements Metadata Store data access functionality."""
import json
import logging

from dkist_processing_common._util.config import get_mesh_config
from dkist_processing_common._util.graphql import GraphQLClient
from dkist_processing_common.models.graphql import CreateRecipeRunStatusResponse
from dkist_processing_common.models.graphql import DatasetCatalogReceiptAccountMutation
from dkist_processing_common.models.graphql import InputDatasetPartResponse
from dkist_processing_common.models.graphql import QualityReportMutation
from dkist_processing_common.models.graphql import QualityReportQuery
from dkist_processing_common.models.graphql import QualityReportResponse
from dkist_processing_common.models.graphql import RecipeRunMutation
from dkist_processing_common.models.graphql import RecipeRunProvenanceMutation
from dkist_processing_common.models.graphql import RecipeRunQuery
from dkist_processing_common.models.graphql import RecipeRunResponse
from dkist_processing_common.models.graphql import RecipeRunStatusMutation
from dkist_processing_common.models.graphql import RecipeRunStatusQuery
from dkist_processing_common.models.graphql import RecipeRunStatusResponse
from dkist_processing_common.models.quality_json_encoders import QualityReportEncoder


logger = logging.getLogger(__name__)

input_dataset_part_document_type_hint = list | dict | str | int | float | None


class MetadataStoreMixin:
    """Mixin for a WorkflowDataTaskBase subclass which implements Metadata Store data access functionality."""

    @property
    def metadata_store_client(self) -> GraphQLClient:
        """Get the graphql client."""
        mesh_config = get_mesh_config()
        return GraphQLClient(
            f'http://{mesh_config["internal-api-gateway"]["mesh_address"]}:{mesh_config["internal-api-gateway"]["mesh_port"]}/graphql'
        )

    def metadata_store_change_recipe_run_to_inprogress(self):
        """Set the recipe run status to "INPROGRESS"."""
        self._metadata_store_change_status(status="INPROGRESS", is_complete=False)

    def metadata_store_change_recipe_run_to_completed_successfully(self):
        """Set the recipe run status to "COMPLETEDSUCCESSFULLY"."""
        self._metadata_store_change_status(status="COMPLETEDSUCCESSFULLY", is_complete=True)

    def metadata_store_add_dataset_receipt_account(
        self, dataset_id: str, expected_object_count: int
    ):
        """Set the number of expected objects."""
        self.metadata_store_client.execute_gql_mutation(
            mutation_base="createDatasetCatalogReceiptAccount",
            mutation_parameters=DatasetCatalogReceiptAccountMutation(
                datasetId=dataset_id, expectedObjectCount=expected_object_count
            ),
        )

    def metadata_store_record_provenance(self, is_task_manual: bool, library_versions: str):
        """Record the provenance record in the metadata store."""
        params = RecipeRunProvenanceMutation(
            inputDatasetId=self.metadata_store_input_dataset_id,
            isTaskManual=is_task_manual,
            recipeRunId=self.recipe_run_id,
            taskName=self.task_name,
            libraryVersions=library_versions,
            workflowVersion=self.workflow_version,
        )
        self.metadata_store_client.execute_gql_mutation(
            mutation_base="createRecipeRunProvenance", mutation_parameters=params
        )

    def metadata_store_add_quality_report(self, dataset_id: str, quality_report: list[dict]):
        """Add the quality report to the metadatastore."""
        quality_report_json = json.dumps(quality_report, cls=QualityReportEncoder, allow_nan=False)
        params = QualityReportMutation(datasetId=dataset_id, qualityReport=quality_report_json)
        self.metadata_store_client.execute_gql_mutation(
            mutation_base="createQualityReport", mutation_parameters=params
        )

    def metadata_store_quality_report_exists(self, dataset_id: str) -> bool:
        """Return True if a quality report exists in the metadata-store for the input dataset id."""
        params = QualityReportQuery(datasetId=dataset_id)
        response = self.metadata_store_client.execute_gql_query(
            query_base="qualityReports",
            query_response_cls=QualityReportResponse,
            query_parameters=params,
        )
        return bool(response)

    def metadata_store_recipe_run_configuration(self) -> dict:
        """Get the recipe run configuration from the metadata store."""
        configuration_json = self._metadata_store_recipe_run().configuration
        if configuration_json is None:
            return {}
        try:
            configuration = json.loads(configuration_json)
            if not isinstance(configuration, dict):
                raise ValueError(
                    f"Invalid recipe run configuration format.  "
                    f"Expected json encoded dictionary, received json encoded {type(configuration)}"
                )
            return configuration
        except (json.JSONDecodeError, ValueError, TypeError, UnicodeDecodeError) as e:
            logger.error(f"Invalid recipe run configuration")
            raise e

    @property
    def metadata_store_input_dataset_parts(self) -> list[InputDatasetPartResponse]:
        """Get the input dataset parts from the metadata store."""
        return [
            part_link.inputDatasetPart
            for part_link in self._metadata_store_recipe_run().recipeInstance.inputDataset.inputDatasetInputDatasetParts
        ]

    def _metadata_store_filter_input_dataset_parts(
        self, input_dataset_part_type_name: str
    ) -> InputDatasetPartResponse | list[InputDatasetPartResponse] | None:
        """Filter the input dataset parts based on the input dataset part type name."""
        target_parts = [
            part
            for part in self.metadata_store_input_dataset_parts
            if part.inputDatasetPartType.inputDatasetPartTypeName == input_dataset_part_type_name
        ]
        if not target_parts:
            return
        if len(target_parts) == 1:
            return target_parts[0]
        raise ValueError(
            f"Multiple ({len(target_parts)}) input dataset parts found for "
            f"{input_dataset_part_type_name=}."
        )

    @property
    def _metadata_store_input_dataset_observe_frames_part(
        self,
    ) -> InputDatasetPartResponse | None:
        """Get the input dataset part for observe frames."""
        return self._metadata_store_filter_input_dataset_parts(
            input_dataset_part_type_name="observe_frames",
        )

    @property
    def metadata_store_input_dataset_observe_frames_part_id(self) -> int | None:
        """Get the input dataset part id for observe frames."""
        if part := self._metadata_store_input_dataset_observe_frames_part:
            return part.inputDatasetPartId

    @property
    def metadata_store_input_dataset_observe_frames_part_document(
        self,
    ) -> input_dataset_part_document_type_hint:
        """Get the input dataset part document for observe frames."""
        if part := self._metadata_store_input_dataset_observe_frames_part:
            return part.inputDatasetPartDocument

    @property
    def _metadata_store_input_dataset_calibration_frames_part(
        self,
    ) -> InputDatasetPartResponse | None:
        """Get the input dataset part for calibration frames."""
        return self._metadata_store_filter_input_dataset_parts(
            input_dataset_part_type_name="calibration_frames"
        )

    @property
    def metadata_store_input_dataset_calibration_frames_part_id(self) -> int | None:
        """Get the input dataset part id for calibration frames."""
        if part := self._metadata_store_input_dataset_calibration_frames_part:
            return part.inputDatasetPartId

    @property
    def metadata_store_input_dataset_calibration_frames_part_document(
        self,
    ) -> input_dataset_part_document_type_hint:
        """Get the input dataset part document for calibration frames."""
        if part := self._metadata_store_input_dataset_calibration_frames_part:
            return part.inputDatasetPartDocument

    @property
    def _metadata_store_input_dataset_parameters_part(
        self,
    ) -> InputDatasetPartResponse | None:
        """Get the input dataset part for parameters."""
        return self._metadata_store_filter_input_dataset_parts(
            input_dataset_part_type_name="parameters"
        )

    @property
    def metadata_store_input_dataset_parameters_part_id(self) -> int | None:
        """Get the input dataset part id for parameters."""
        if part := self._metadata_store_input_dataset_parameters_part:
            return part.inputDatasetPartId

    @property
    def metadata_store_input_dataset_parameters_part_document(
        self,
    ) -> input_dataset_part_document_type_hint:
        """Get the input dataset part document for parameters."""
        if part := self._metadata_store_input_dataset_parameters_part:
            return part.inputDatasetPartDocument

    @property
    def metadata_store_input_dataset_id(self) -> int:
        """Get the input dataset id from the metadata store."""
        return self._metadata_store_recipe_run().recipeInstance.inputDataset.inputDatasetId

    @property
    def metadata_store_recipe_instance_id(self) -> int:
        """Get the recipe instance id from the metadata store."""
        return self._metadata_store_recipe_run().recipeInstanceId

    @property
    def metadata_store_recipe_id(self) -> int:
        """Get the recipe id from the metadata store."""
        return self._metadata_store_recipe_run().recipeInstance.recipeId

    def _metadata_store_recipe_run(self, allow_cache: bool = True) -> RecipeRunResponse:
        is_cached = bool(getattr(self, "_recipe_run_cache", False))
        if is_cached and allow_cache:
            return self._recipe_run_cache
        response = self.metadata_store_client.execute_gql_query(
            query_base="recipeRuns",
            query_response_cls=RecipeRunResponse,
            query_parameters=RecipeRunQuery(recipeRunId=self.recipe_run_id),
        )
        self._recipe_run_cache = response[0]
        return self._recipe_run_cache

    def _metadata_store_change_status(self, status: str, is_complete: bool):
        """Change the recipe run status of a recipe run to the given status."""
        recipe_run_status_id = self._metadata_store_recipe_run_status_id(status=status)
        if not recipe_run_status_id:
            recipe_run_status_id = self._metadata_store_create_recipe_run_status(
                status=status, is_complete=is_complete
            )
        self._metadata_store_update_status(recipe_run_status_id=recipe_run_status_id)

    def _metadata_store_recipe_run_status_id(self, status: str) -> None | int:
        """Find the id of a recipe run status."""
        response = self.metadata_store_client.execute_gql_query(
            query_base="recipeRunStatuses",
            query_response_cls=RecipeRunStatusResponse,
            query_parameters=RecipeRunStatusQuery(recipeRunStatusName=status),
        )
        if len(response) > 0:
            return response[0].recipeRunStatusId

    def _metadata_store_create_recipe_run_status(self, status: str, is_complete: bool) -> int:
        """
        Add a new recipe run status to the db.

        :param status: name of the status to add
        :param is_complete: does the new status correspond to an accepted completion state
        """
        recipe_run_statuses = {
            "INPROGRESS": "Recipe run is currently undergoing processing",
            "COMPLETEDSUCCESSFULLY": "Recipe run processing completed with no errors",
        }

        if not isinstance(status, str):
            raise TypeError(f"status must be of type str: {status}")
        if not isinstance(is_complete, bool):
            raise TypeError(f"is_complete must be of type bool: {is_complete}")
        recipe_run_status_response = self.metadata_store_client.execute_gql_mutation(
            mutation_base="createRecipeRunStatus",
            mutation_response_cls=CreateRecipeRunStatusResponse,
            mutation_parameters=RecipeRunStatusMutation(
                recipeRunStatusName=status,
                isComplete=is_complete,
                recipeRunStatusDescription=recipe_run_statuses[status],
            ),
        )
        return recipe_run_status_response.recipeRunStatus.recipeRunStatusId

    def _metadata_store_update_status(
        self,
        recipe_run_status_id: int,
    ):
        """
        Change the status of a given recipe run id.

        :param recipe_run_status_id: the new status to use
        :param recipe_run_id: id of the recipe run to have the status changed
        """
        self.metadata_store_client.execute_gql_mutation(
            mutation_base="updateRecipeRun",
            mutation_parameters=RecipeRunMutation(
                recipeRunId=self.recipe_run_id, recipeRunStatusId=recipe_run_status_id
            ),
        )
