
@pytest.mark.parametrize("configure_servers", [1], indirect=["configure_servers"])
def test_sync_workbooks_after_delete_overlapping_workbook_in_default_server(configure_servers):
    """Sync workbooks after deleted overlapping workbook.

    As a user, I want to sync workbooks after deleting overlapping workbooks in PAOS app and on default server

    AUTHOR: Mehul Bansal

    Args:
        configure_servers (Any): Fixture for configuring Phantom servers.
    """
    web_driver = "chrome_driver"
    workbook_page = WorkbookPage(dreiver=web_driver)
    assert_utility = AssertUtility(phantom_server_list=[0], driver=web_driver)

    # create workbooks on default server
    workbook_page.workbook_table.phantom_workbook_api_helper.create_workbooks(workbook_list=[1, 2, 3, 4, 5], phantom_server=0)

    # Go to workbook page and sync workbook.
    workbook_page.go_to_page()
    workbook_page.sync_workbooks()

    # Check workbooks are synced
    assert_utility.assert_message(message="Sync Successfully")
    assert_utility.assert_workbook_after_sync(
        published=[1, 2, 3, 4, 5],
        deleted=[],
        purged=[]
    )

    # Delete workbooks
    workbook_page.workbook_table.phantom_workbook_api_helper.delete_workbooks(workbook_names=[1, 2], phantom_server=0)

    # Delete workbooks in the PAOS app and then click on save and sync.
    workbook_page.workbook_table.delete_workbooks(workbook_names=[1, 2, 5])
    workbook_page.save_and_sync_workbooks()

    # Check workbook are synced
    assert_utility.assert_workbook_after_delete(
        published=[3, 4],
        deleted=[1, 2, 5],
        purged=[]
    )

    # Confirm that the deleted workbooks are allowed to restore in PAOS app.
    Deleted_workbooks = ["1", "2", "5"]
    for name in Deleted_workbooks:
        assert workbook_page.workbooks_table.is_action_enabled(workbook_name=name, action=WorkbookActions.RESTORE)



@pytest.mark.parametrize("configure_servers", [4], indirect=["configure_servers"])
def test_sync_workbooks_after_delete_unique_workbooks_in_multiple_nonDefault_server(configure_servers):
    """Sync_workbooks_after_delete_unique_workbooks_in_multiple_nonDefault_server.

    As a user, I want to sync workbooks after deleting unique workbooks in PAOS app and multiple non-default servers, and default server

    AUTHOR: Mehul Bansal

    Args:
        configure_servers (Any): Fixture for configuring Phantom servers.
    """
    web_driver = "chrome_driver"
    workbook_page = WorkbookPage(dreiver=web_driver)
    assert_utility = AssertUtility(phantom_server_list=[0, 1, 2, 3], driver=web_driver)

    # create workbooks on default server
    workbook_page.workbook_table.phantom_workbook_api_helper.create_workbooks(workbook_list=[1, 2], phantom_server=0)

    # create workbooks on non default server
    workbook_page.workbook_table.phantom_workbook_api_helper.create_workbooks(workbook_list=[3, 4], phantom_server=1)

    # create workbooks on non default server
    workbook_page.workbook_table.phantom_workbook_api_helper.create_workbooks(workbook_list=[5, 6], phantom_server=2)

    # create workbooks on non default server
    workbook_page.workbook_table.phantom_workbook_api_helper.create_workbooks(workbook_list=[7, 8], phantom_server=3)

    # Go to workbook page and sync workbooks.
    workbook_page.go_to_page()
    workbook_page.sync_workbooks()

    # Check workbooks are synced
    assert_utility.assert_message(message="Sync Successfully")
    assert_utility.assert_workbook_after_sync(
        published=[1, 2, 3, 4, 5, 6, 7, 8],
        deleted=[],
        purged=[]
    )

    # Delete workbooks from the servers.
    workbook_page.workbook_table.phantom_workbook_api_helper.delete_workbooks(workbook_names=[1, 2], phantom_server=1)
    workbook_page.workbook_table.phantom_workbook_api_helper.delete_workbooks(workbook_names=[3, 4], phantom_server=2)
    workbook_page.workbook_table.phantom_workbook_api_helper.delete_workbooks(workbook_names=[5, 6], phantom_server=3)
    workbook_page.workbook_table.phantom_workbook_api_helper.delete_workbooks(workbook_names=[1, 2, 3, 4, 5], phantom_server=0)

    # Delete workbooks in the PAOS app and then click on save and sync.
    workbook_page.workbook_table.delete_workbooks(workbook_names=[7])
    workbook_page.save_and_sync_workbooks()

    # Check workbook are synced
    assert_utility.assert_workbook_after_delete(
        published=[6, 8],
        deleted=[1, 2, 3, 4, 5, 7],
        purged=[]
    )

    # Confirm that the deleted workbooks are allowed to restore in PAOS app.
    Deleted_workbooks = ["1", "2", "3", "4", "5", "7"]
    for name in Deleted_workbooks:
        assert workbook_page.workbooks_table.is_action_enabled(workbook_name=name, action=WorkbookActions.RESTORE)












# 1st.
@pytest.mark.parametrize("configure_servers", [1], indirect=["configure_servers"])
def test_restore_multiple_workbooks_with_single_default_server(configure_servers):
    """Restore multiple workbooks with single configured default server.

    As a user, I want to restore a multiple workbooks from a single configured Phantom server

    AUTHOR: Mehul Bansal

    Args:
        configure_servers (Any): Fixture for configuring Phantom servers.
    """
    web_driver = "chrome_driver"
    workbook_page = WorkbookPage(dreiver=web_driver)
    assert_utility = AssertUtility(phantom_server_list=[0], driver=web_driver)

    # create workbooks on default server
    workbook_page.workbook_table.phantom_workbook_api_helper.create_workbooks(workbook_list=list(range(1, 11)), phantom_server=0)

    # Go to workbook page and sync workbook.
    workbook_page.go_to_page()
    workbook_page.sync_workbooks()

    # Check workbooks are synced
    assert_utility.assert_message(message="Sync Successfully")
    assert_utility.assert_workbook_after_sync(
        published=list(range(1, 11)),
        deleted=[],
        purged=[]
    )

    # Store random workbooks content for future comparison
    initial_workbooks_content = workbook_page.phantom_workbook_api_helper.get_workbooks(phantom_server=0, workbook_list=[1, 2, 3, 4, 5, 7, 8, 9, 10])

    # Delete workbooks in the PAOS app and then click on save and sync.
    workbook_page.workbook_table.delete_workbooks(workbook_names=[1, 4, 6])
    workbook_page.save_and_sync_workbooks()

    # Check workbook are synced
    assert_utility.assert_workbook_after_delete(
        published=[2, 3, 5, 7, 8, 9, 10],
        deleted=[1, 4, 6],
        purged=[]
    )

    # Confirm that the deleted workbooks are allowed to restore in PAOS app.
    Deleted_workbooks = ["1", "4", "6"]
    for name in Deleted_workbooks:
        assert workbook_page.workbooks_table.is_action_enabled(workbook_name=name, action=WorkbookActions.RESTORE)

    # Delete workbooks in the PAOS app and then click on save and sync.
    workbook_page.workbook_table.restore_workbooks(workbook_names=[1, 4])
    workbook_page.save_and_sync_workbooks()

    # Check workbook are synced
    assert_utility.assert_workbook_after_sync(
        published=[1, 2, 3, 4, 5, 7, 8, 9, 10],
        deleted=[6],
        purged=[]
    )

    # Restored workbooks content and Check.
    workbook_restored = workbook_page.phantom_workbook_api_helper.get_workbooks(phantom_server=0,
                                                                                workbook_name_list=[1, 4])

    assert_utility.assert_workbook_after_restore(
        published=[1, 2, 3, 4, 5, 7, 8, 9, 10],
        deleted=[6],
        json_content=workbook_restored
    )

    # Get all workbooks content for comparison
    final_workbooks_content = workbook_page.phantom_workbook_api_helper.get_workbooks(phantom_server=0)

    # replace final workbooks content with prior to delete content
    updated_json = assert_utility.replace_updated_workbooks(
        old_workbooks=final_workbooks_content, updated_workbooks=initial_workbooks_content
    )

    # Checking workbooks are present in phantom.conf
    assert_utility.assert_workbooks_in_phantom_conf(Json_object_with_updated_content=updated_json)

    # Checking updated workbooks' content with phantom servers and phantom.conf
    assert_utility.assert_workbooks_exact_content_in_phantom_server(workbook_name_list=[1, 4])





# 2nd.
@pytest.mark.parametrize("configure_servers", [1], indirect=["configure_servers"])
def test_sync_workbooks_after_delete_adding_overlapping_workbooks_with_single_default_server(configure_servers):
    """Restore multiple workbooks with single configured default server.

    As a user, I want to sync workbooks after deleting and adding overlapping workbooks in PAOS app and on default server

    AUTHOR: Mehul Bansal

    Args:
        configure_servers (Any): Fixture for configuring Phantom servers.
    """
    web_driver = "chrome_driver"
    workbook_page = WorkbookPage(dreiver=web_driver)
    assert_utility = AssertUtility(phantom_server_list=[0], driver=web_driver)

    # create workbooks on default server
    workbook_page.workbook_table.phantom_workbook_api_helper.create_workbooks(workbook_list=[1, 2, 3, 4, 5], phantom_server=0)

    # Go to workbook page and sync workbook.
    workbook_page.go_to_page()
    workbook_page.sync_workbooks()

    # Check workbooks are synced
    assert_utility.assert_message(message="Sync Successfully")
    assert_utility.assert_workbook_after_sync(
        published=[1, 2, 3, 4, 5],
        deleted=[],
        purged=[]
    )

    # Delete workbooks in the PAOS app and then click on save and sync.
    workbook_page.workbook_table.delete_workbooks(workbook_names=[1, 2, 5])
    workbook_page.save_and_sync_workbooks()

    # Check workbook are synced
    assert_utility.assert_workbook_after_delete(
        published=[3, 4],
        deleted=[1, 2, 5],
        purged=[]
    )

    # Confirm that the deleted workbooks are allowed to restore in PAOS app.
    Deleted_workbooks = ["1", "2", "5"]
    for name in Deleted_workbooks:
        assert workbook_page.workbooks_table.is_action_enabled(workbook_name=name, action=WorkbookActions.RESTORE)

    # create workbooks on default server and then sync workbooks.
    workbook_page.workbook_table.phantom_workbook_api_helper.create_workbooks(workbook_list=[1, 2], phantom_server=0)
    workbook_page.sync_workbooks()

    # Check workbook are synced
    assert_utility.assert_message(message="Sync Successfully")
    assert_utility.assert_workbook_after_sync(
        published=[1, 2, 3, 4],
        deleted=[5],
        purged=[]
    )
