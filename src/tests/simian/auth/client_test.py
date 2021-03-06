#!/usr/bin/env python
# 
# Copyright 2010 Google Inc. All Rights Reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# #

"""client module tests."""



import logging
logging.basicConfig(filename='/dev/null')

from google.apputils import app
from google.apputils import basetest
import mox
import stubout

from simian.auth import client
from tests.simian import test_settings


class AuthSessionSimianClientTest(mox.MoxTestBase):
  """Test AuthSessionSimianClient class."""

  def testBasic(self):
    self.assertTrue(issubclass(
        client.AuthSessionSimianClient, client.base.Auth1ClientSession))


class AuthSimianClientTest(mox.MoxTestBase):
  """Test AuthSimianClient class."""

  def setUp(self):
    mox.MoxTestBase.setUp(self)
    self.stubs = stubout.StubOutForTesting()
    self.apc = client.AuthSimianClient()

  def tearDown(self):
    self.mox.UnsetStubs()
    self.stubs.UnsetAll()

  def testGetSessionClass(self):
    self.assertTrue(
        self.apc.GetSessionClass() is client.AuthSessionSimianClient)

  def testLoadCaParameters(self):
    """Test _LoadCaParameters()."""
    self.mox.ReplayAll()
    self.apc.LoadCaParameters(test_settings)
    self.assertEqual(self.apc._ca_pem, test_settings.CA_PUBLIC_CERT_PEM)
    self.assertEqual(
        self.apc._server_cert_pem, test_settings.SERVER_PUBLIC_CERT_PEM)
    self.assertEqual(
        self.apc._required_issuer, test_settings.REQUIRED_ISSUER)
    self.mox.VerifyAll()

  def testLoadCaParametersWhenError(self):
    """Test _LoadCaParameters()."""
    self.mox.StubOutWithMock(client.util, 'GetCaParameters')

    client.util.GetCaParameters(
        test_settings).AndRaise(client.util.CaParametersError)

    self.mox.ReplayAll()
    self.assertRaises(
        client.CaParametersError, self.apc.LoadCaParameters, test_settings)
    self.mox.VerifyAll()


def main(unused_argv):
  basetest.main()


if __name__ == '__main__':
  app.run()