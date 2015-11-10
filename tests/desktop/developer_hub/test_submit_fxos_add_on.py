# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import shutil
import uuid
import warnings
from zipfile import ZipFile

import pytest

from pages.desktop.developer_hub.content_tools import ContentTools
from tests.base_test import BaseTest


class TestSubmitFxOSAddOn(BaseTest):

    @pytest.fixture
    def add_on(self, request, tmpdir):

        add_on_name = str(uuid.uuid4())
        new_zip_path = str(tmpdir.join('%s.zip' % add_on_name))

        # copy zip file to tmpdir
        shutil.copyfile(self._get_resource_path('fxosaddon.zip'), new_zip_path)

        # update manifest.json in zip file
        with ZipFile(new_zip_path, 'a') as zipfile:
            data = json.loads(zipfile.read('manifest.json'))
            data['name'] = add_on_name
            # ignore warning that's issued for overwriting the manifest.json file
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                zipfile.writestr('manifest.json', json.dumps(data))

        return {'name': add_on_name, 'path': new_zip_path}

    @pytest.mark.credentials
    def test_add_on_submission(self, mozwebqa, new_user, add_on):
        page = ContentTools(mozwebqa).go_to_page()
        page.login(mozwebqa, new_user['email'], new_user['password'])
        page.click_submit_new_add_on()
        page.click_agree()
        page.select_add_on_file(add_on['path'])
        page.click_submit_add_on_form_button()
        assert 'success' in page.notification_message
        new_add_on = page.add_on(add_on['name'])
        assert 'pending' == new_add_on.status.lower()
        new_add_on.delete()
