from typing import Union, Optional

from orkg.common import OID
from orkg.out import OrkgResponse
from orkg.utils import NamespacedClient
from orkg.client.harvesters import doi as doi_harvester


class HarvestersClient(NamespacedClient):

    def doi_harvest(self, doi: str, orkg_rf: Union[str, OID], directory: Optional[str]) -> OrkgResponse:
        """
        Harvests DOI data for a paper and add it to the ORKG.
        It works under the assumption that the paper contains some JSON-LD representation of its content
        If directory is provided, it is expected to have a `doi.json` file and other json files that are the contributions.
        If the `doi.json` doesn't exist and the `doi` parameter is present then the metadata is fetched from the DOI and the contributions from disk.
        :param doi: The DOI of the paper to harvest
        :param orkg_rf: The resource ID of the ORKG research field to add the harvested data to, or the string representation to be looked up (can raise errors)
        :param directory: The directory to read the specs from (optional)
        """
        return doi_harvester.harvest(self.client, doi, orkg_rf, directory)
