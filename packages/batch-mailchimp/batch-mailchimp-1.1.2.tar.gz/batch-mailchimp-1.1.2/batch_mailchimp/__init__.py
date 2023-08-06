import json
import uuid
from six.moves.urllib.parse import urlparse
from mailchimp_marketing.api.surveys_api import SurveysApi
from mailchimp_marketing.api.account_export_api import AccountExportApi
from mailchimp_marketing.api.account_exports_api import AccountExportsApi
from mailchimp_marketing.api.activity_feed_api import ActivityFeedApi
from mailchimp_marketing.api.authorized_apps_api import AuthorizedAppsApi
from mailchimp_marketing.api.automations_api import AutomationsApi
from mailchimp_marketing.api.batch_webhooks_api import BatchWebhooksApi
from mailchimp_marketing.api.campaign_folders_api import CampaignFoldersApi
from mailchimp_marketing.api.campaigns_api import CampaignsApi
from mailchimp_marketing.api.connected_sites_api import ConnectedSitesApi
from mailchimp_marketing.api.conversations_api import ConversationsApi
from mailchimp_marketing.api.customer_journeys_api import CustomerJourneysApi
from mailchimp_marketing.api.ecommerce_api import EcommerceApi
from mailchimp_marketing.api.facebook_ads_api import FacebookAdsApi
from mailchimp_marketing.api.file_manager_api import FileManagerApi
from mailchimp_marketing.api.landing_pages_api import LandingPagesApi
from mailchimp_marketing.api.lists_api import ListsApi
from mailchimp_marketing.api.ping_api import PingApi
from mailchimp_marketing.api.reporting_api import ReportingApi
from mailchimp_marketing.api.reports_api import ReportsApi
from mailchimp_marketing.api.root_api import RootApi
from mailchimp_marketing.api.search_campaigns_api import SearchCampaignsApi
from mailchimp_marketing.api.search_members_api import SearchMembersApi
from mailchimp_marketing.api.template_folders_api import TemplateFoldersApi
from mailchimp_marketing.api.templates_api import TemplatesApi
from mailchimp_marketing.api.verified_domains_api import VerifiedDomainsApi
from mailchimp_marketing import api_client
from mailchimp_marketing import Client as MailChimpClient
from .batches_api import BatchesApi


class FakeRequest:
    def __init__(self, operation_id):
        self.ok = True
        self.headers = {
            "content-type": "application/json"
        }
        self._operation_id = operation_id

    def json(self):
        return {
            "okay": True,
            "operation_id": self._operation_id,
        }


class ApiClient(api_client.ApiClient):
    def __init__(self, config={}):
        self.operations = []
        self.set_batch_mode(config.get("batch", False))
        super().__init__(config)

    def set_batch_mode(self, state):
        self.batch_mode = state

    def set_config(self, config={}):
        if "batch" in config:
            if self.operations and not config["batch"]:
                raise Exception("Can’t disable batch mode")
            self.batch_mode = config["batch"]
        super().set_config(config)

    def request(self, method, url, query_params=None, headers=None, body=None):
        if not self.batch_mode:
            return super().request(method, url, query_params, headers, body)
        operation = {
            "method": method,
            "path": urlparse(url).path[4:],
            "operation_id": uuid.uuid4().hex,
        }
        if query_params:
            operation["params"] = dict(query_params)
        if body:
            operation["body"] = json.dumps(body)

        self.operations.append(operation)
        return FakeRequest(operation["operation_id"])


class Client(MailChimpClient):
    def __init__(self, config={}):
        self.api_client = ApiClient(config)

        self.Surveys = SurveysApi(self.api_client)
        self.accountExport = AccountExportApi(self.api_client)
        self.accountExports = AccountExportsApi(self.api_client)
        self.activityFeed = ActivityFeedApi(self.api_client)
        self.authorizedApps = AuthorizedAppsApi(self.api_client)
        self.automations = AutomationsApi(self.api_client)
        self.batchWebhooks = BatchWebhooksApi(self.api_client)
        self.batches = BatchesApi(self.api_client)
        self.campaignFolders = CampaignFoldersApi(self.api_client)
        self.campaigns = CampaignsApi(self.api_client)
        self.connectedSites = ConnectedSitesApi(self.api_client)
        self.conversations = ConversationsApi(self.api_client)
        self.customerJourneys = CustomerJourneysApi(self.api_client)
        self.ecommerce = EcommerceApi(self.api_client)
        self.facebookAds = FacebookAdsApi(self.api_client)
        self.fileManager = FileManagerApi(self.api_client)
        self.landingPages = LandingPagesApi(self.api_client)
        self.lists = ListsApi(self.api_client)
        self.ping = PingApi(self.api_client)
        self.reporting = ReportingApi(self.api_client)
        self.reports = ReportsApi(self.api_client)
        self.root = RootApi(self.api_client)
        self.searchCampaigns = SearchCampaignsApi(self.api_client)
        self.searchMembers = SearchMembersApi(self.api_client)
        self.templateFolders = TemplateFoldersApi(self.api_client)
        self.templates = TemplatesApi(self.api_client)
        self.verifiedDomains = VerifiedDomainsApi(self.api_client)
        self.batches = BatchesApi(self.api_client)

    def __repr__(self):
        return "<{module}.{name}: batch mode {batch_mode_toggle}>".format(
            module=self.__class__.__module__,
            name=self.__class__.__name__,
            batch_mode_toggle="ON" if self.api_client.batch_mode else "OFF",
        )
