from Core.reporting.dashboard.data_collection.helpers.jira import *
from Core.reporting.dashboard.data_collection.job_manager import *
from enum import Enum


class UseJIRAFilters(Enum):
    """
    These are id mapping from existing JIRA filters that current user can access
    """
    QA_UAT_ISSUES_ASSIGNED_TO_QA = 23723
    QA_BUGS_TO_BE_ASSIGNED_TO_QA_ALL_ENVIRONMENTS = 23724
    QA_CDA_CTA_BUGS_CURRENTLY_ASSIGNED_TO_QA = 23725
    QA_SME_ENHANCEMENTS_FOR_ALL_ENVIRONMENTS = 23611


def run_qa_bugs_to_be_assigned_to_qa_all_environments():
    query_filter = jira_server.get_issue_filter(UseJIRAFilters.QA_BUGS_TO_BE_ASSIGNED_TO_QA_ALL_ENVIRONMENTS.value)
    send_tickets_to_elastic_index_from_query(query=query_filter.jql,
                                             index_name='{0}_{1}'.format(
                                                 INDEX_NAME_JIRA,
                                                 run_qa_bugs_to_be_assigned_to_qa_all_environments.__name__
                                                )
                                             )


def run_qa_cda_cta_bugs_currently_assigned_to_qa():
    query_filter = jira_server.get_issue_filter(UseJIRAFilters.QA_CDA_CTA_BUGS_CURRENTLY_ASSIGNED_TO_QA.value)
    send_tickets_to_elastic_index_from_query(query=query_filter.jql,
                                             index_name='{0}_{1}'.format(
                                                 INDEX_NAME_JIRA,
                                                 run_qa_cda_cta_bugs_currently_assigned_to_qa.__name__
                                                )
                                             )


def run_qa_sme_enhancements_for_all_environments():
    query_filter = jira_server.get_issue_filter(UseJIRAFilters.QA_SME_ENHANCEMENTS_FOR_ALL_ENVIRONMENTS.value)
    send_tickets_to_elastic_index_from_query(query=query_filter.jql,
                                             index_name='{0}_{1}'.format(
                                                 INDEX_NAME_JIRA,
                                                 run_qa_sme_enhancements_for_all_environments.__name__
                                                )
                                             )


def run_qa_uat_issues_assigned_to_qa():
    query_filter = jira_server.get_issue_filter(UseJIRAFilters.QA_UAT_ISSUES_ASSIGNED_TO_QA.value)
    send_tickets_to_elastic_index_from_query(query=query_filter.jql,
                                             index_name='{0}_{1}'.format(
                                                 INDEX_NAME_JIRA,
                                                 run_qa_uat_issues_assigned_to_qa.__name__
                                                )
                                             )