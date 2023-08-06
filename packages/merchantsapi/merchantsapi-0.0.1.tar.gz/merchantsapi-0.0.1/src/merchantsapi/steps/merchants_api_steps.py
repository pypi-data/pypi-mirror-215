from pytest_bdd import given, then, parsers
from merchantsapi.fixtures import * 
from qashared.fixtures import *
from qashared.assertions import *

@given('I use the merchants api to create a new application')
def create_new_application(merchants_api: any, test_data: any, application_context: any, target_fixture="application_context"):
    application_context.application = merchants_api.applications.create(application=test_data.new_application.as_json)
    return application_context

@then(parsers.parse('The application has status "{expected_status}"'))
def check_status(merchants_api: any, application_context: any, expected_status):
    created_application = merchants_api.applications.get(application_context.application.data.id)
    actual_status = created_application.data.current_status
    assert actual_status == expected_status, f'Expected application to have status "{expected_status}", but was "{actual_status}"'

@then('The application data is correct')
def check_data(merchants_api: any, test_data: any, application_context: any):
    created_application = merchants_api.applications.get(application_context.application.data.id)
    
    assert_are_equivalent(created_application, test_data.expected_application.as_object, exclude_paths = [
        "data.id", "data.token", "data.urls.application_url", "data.created_at", "data.updated_at", "data.application_histories", "data.metadata.documents", "data.submissions"
        ])
    assert_matching_attributes(created_application, application_context.application, include_paths=[
        'data.id', 'data.token', 'data.urls.application_url', 'data.created_at'
        ])

@then('The test fails')
def check_data(merchants_api: any, test_data: any, application_context: any):
    created_application = merchants_api.applications.get(application_context.application.data.id)

    test_data.expected_application.as_object.data.current_status = 'REJECTED' # cause data comparison to fail due to values_changed
    created_application.data.new_field = 'TEST_NEW_FIELD' # cause data comparison to fail due to attribute_removed
    test_data.expected_application.as_object.missing_field = 'TEST_MISSING_FIELD'# cause data comparison to fail due to attribute_added

    assert_are_equivalent(created_application, test_data.expected_application.as_object, exclude_paths = [
        "data.id", "data.token", "data.urls.application_url", "data.created_at", "data.updated_at", "data.application_histories", "data.metadata.documents", "data.submissions"
        ])
    assert_matching_attributes(created_application, application_context.application, include_paths=[
        'data.id', 'data.token', 'data.urls.application_url', 'data.created_at'
        ])
    
@then('The test fails for a different reason')
def check_data(merchants_api: any, test_data: any, application_context: any):
    created_application = merchants_api.applications.get(application_context.application.data.id)

    assert_are_equivalent(created_application, test_data.expected_application.as_object, exclude_paths = [
        "data.id", "data.token", "data.urls.application_url", "data.created_at", "data.updated_at", "data.application_histories", "data.metadata.documents", "data.submissions"
        ])
    
    created_application.data.token = 'INCORRECT_TOKEN'
    created_application.data.missing_attribute = 'TEST'
    assert_matching_attributes(created_application, application_context.application, include_paths=[
        'data.id', 'data.token', 'data.urls.application_url', 'data.created_at', 'data.invalid_attribute', 'data.missing_attribute'
        ])
