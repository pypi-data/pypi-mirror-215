# -*- coding: utf8 -*-
# Copyright (c) 2017-2021 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.abstract_client import AbstractClient
from tencentcloud.ocr.v20181119 import models


class OcrClient(AbstractClient):
    _apiVersion = '2018-11-19'
    _endpoint = 'ocr.tencentcloudapi.com'
    _service = 'ocr'


    def BankCardOCR(self, request):
        """This API is used to detect and recognize key fields such as the card number, bank information, and expiration date on mainstream bank cards in Mainland China.

        This API is not fully available for the time being. For more information, please contact your [Tencent Cloud sales rep](https://intl.cloud.tencent.com/contact-sales).

        :param request: Request instance for BankCardOCR.
        :type request: :class:`tencentcloud.ocr.v20181119.models.BankCardOCRRequest`
        :rtype: :class:`tencentcloud.ocr.v20181119.models.BankCardOCRResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("BankCardOCR", params, headers=headers)
            response = json.loads(body)
            model = models.BankCardOCRResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def GeneralAccurateOCR(self, request):
        """This API is used to detect and recognize characters in an image. It can recognize Chinese, English, Chinese-English, digits, and special symbols and return the text box positions and characters.

        It is suitable for scenarios with a lot of characters in complex layouts and requiring high recognition accuracy, such as examination papers, online images, signboards, and legal documents.

        Strengths: compared with general print recognition, it provides higher-precision character recognition services. Its accuracy and recall rate are higher in difficult scenarios such as a large number of characters, long strings of digits, small characters, blurry characters, and tilted text.

        This API is not fully available for the time being. For more information, please contact your [Tencent Cloud sales rep](https://intl.cloud.tencent.com/contact-sales).

        :param request: Request instance for GeneralAccurateOCR.
        :type request: :class:`tencentcloud.ocr.v20181119.models.GeneralAccurateOCRRequest`
        :rtype: :class:`tencentcloud.ocr.v20181119.models.GeneralAccurateOCRResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GeneralAccurateOCR", params, headers=headers)
            response = json.loads(body)
            model = models.GeneralAccurateOCRResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def GeneralBasicOCR(self, request):
        """This API is used to detect and recognize characters in an image in the following 20 languages: Chinese, English, Japanese, Korean, Spanish, French, German, Portuguese, Vietnamese, Malay, Russian, Italian, Dutch, Swedish, Finnish, Danish, Norwegian, Hungarian, Thai, and Arabic. Mixed characters in English and each supported language can be recognized together.

        It can recognize printed text in paper documents, online images, ads, signboards, menus, video titles, profile photos, etc.

        Strengths: it can automatically recognize the text language, return the text box coordinate information, and automatically rotate tilted text to the upright direction.

        This API is not fully available for the time being. For more information, please contact your [Tencent Cloud sales rep](https://intl.cloud.tencent.com/contact-sales).

        :param request: Request instance for GeneralBasicOCR.
        :type request: :class:`tencentcloud.ocr.v20181119.models.GeneralBasicOCRRequest`
        :rtype: :class:`tencentcloud.ocr.v20181119.models.GeneralBasicOCRResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GeneralBasicOCR", params, headers=headers)
            response = json.loads(body)
            model = models.GeneralBasicOCRResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def HKIDCardOCR(self, request):
        """This API is used to recognize key fields on the photo side of a Hong Kong (China) identity card, including name in Chinese, name in English, telecode for name, date of birth, gender, document symbol, date of the first issue, date of the last receipt, identity card number, and permanent residency attribute. It can check for card authenticity and crop the identity photo.

        This API is not fully available for the time being. For more information, please contact your [Tencent Cloud sales rep](https://intl.cloud.tencent.com/contact-sales).

        :param request: Request instance for HKIDCardOCR.
        :type request: :class:`tencentcloud.ocr.v20181119.models.HKIDCardOCRRequest`
        :rtype: :class:`tencentcloud.ocr.v20181119.models.HKIDCardOCRResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("HKIDCardOCR", params, headers=headers)
            response = json.loads(body)
            model = models.HKIDCardOCRResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def MLIDCardOCR(self, request):
        """This API is used to recognize a Malaysian identity card, including identity card number, name, gender, and address. It is also used to crop identity photos and give alarms for photographed or photocopied certificates.

        This API is not fully available for the time being. For more information, contact your [Tencent Cloud sales rep](https://intl.cloud.tencent.com/contact-sales).

        :param request: Request instance for MLIDCardOCR.
        :type request: :class:`tencentcloud.ocr.v20181119.models.MLIDCardOCRRequest`
        :rtype: :class:`tencentcloud.ocr.v20181119.models.MLIDCardOCRResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("MLIDCardOCR", params, headers=headers)
            response = json.loads(body)
            model = models.MLIDCardOCRResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def MLIDPassportOCR(self, request):
        """This API is used to recognize a passport issued in Hong Kong/Macao/Taiwan (China) or other countries/regions. Recognizable fields include passport ID, name, date of birth, gender, expiration date, issuing country/region, and nationality. It has the features of cropping identity photos and alarming for photographed or photocopied documents.

        This API is not fully available for the time being. For more information, please contact your [Tencent Cloud sales rep](https://intl.cloud.tencent.com/contact-sales).

        :param request: Request instance for MLIDPassportOCR.
        :type request: :class:`tencentcloud.ocr.v20181119.models.MLIDPassportOCRRequest`
        :rtype: :class:`tencentcloud.ocr.v20181119.models.MLIDPassportOCRResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("MLIDPassportOCR", params, headers=headers)
            response = json.loads(body)
            model = models.MLIDPassportOCRResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RecognizeIndonesiaIDCardOCR(self, request):
        """This API is used to recognize an Indonesian identity card.

        The API request rate is limited to 20 requests/sec by default.

        :param request: Request instance for RecognizeIndonesiaIDCardOCR.
        :type request: :class:`tencentcloud.ocr.v20181119.models.RecognizeIndonesiaIDCardOCRRequest`
        :rtype: :class:`tencentcloud.ocr.v20181119.models.RecognizeIndonesiaIDCardOCRResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RecognizeIndonesiaIDCardOCR", params, headers=headers)
            response = json.loads(body)
            model = models.RecognizeIndonesiaIDCardOCRResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RecognizeKoreanDrivingLicenseOCR(self, request):
        """This API is used to recognize a South Korean driver's license.

        :param request: Request instance for RecognizeKoreanDrivingLicenseOCR.
        :type request: :class:`tencentcloud.ocr.v20181119.models.RecognizeKoreanDrivingLicenseOCRRequest`
        :rtype: :class:`tencentcloud.ocr.v20181119.models.RecognizeKoreanDrivingLicenseOCRResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RecognizeKoreanDrivingLicenseOCR", params, headers=headers)
            response = json.loads(body)
            model = models.RecognizeKoreanDrivingLicenseOCRResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RecognizeKoreanIDCardOCR(self, request):
        """This API is used to recognize a South Korean ID card.

        :param request: Request instance for RecognizeKoreanIDCardOCR.
        :type request: :class:`tencentcloud.ocr.v20181119.models.RecognizeKoreanIDCardOCRRequest`
        :rtype: :class:`tencentcloud.ocr.v20181119.models.RecognizeKoreanIDCardOCRResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RecognizeKoreanIDCardOCR", params, headers=headers)
            response = json.loads(body)
            model = models.RecognizeKoreanIDCardOCRResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RecognizePhilippinesDrivingLicenseOCR(self, request):
        """This API is used to recognize a Philippine driver's license.

        :param request: Request instance for RecognizePhilippinesDrivingLicenseOCR.
        :type request: :class:`tencentcloud.ocr.v20181119.models.RecognizePhilippinesDrivingLicenseOCRRequest`
        :rtype: :class:`tencentcloud.ocr.v20181119.models.RecognizePhilippinesDrivingLicenseOCRResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RecognizePhilippinesDrivingLicenseOCR", params, headers=headers)
            response = json.loads(body)
            model = models.RecognizePhilippinesDrivingLicenseOCRResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RecognizePhilippinesSssIDOCR(self, request):
        """This API is used to recognize a Philippine SSSID/UMID card.

        :param request: Request instance for RecognizePhilippinesSssIDOCR.
        :type request: :class:`tencentcloud.ocr.v20181119.models.RecognizePhilippinesSssIDOCRRequest`
        :rtype: :class:`tencentcloud.ocr.v20181119.models.RecognizePhilippinesSssIDOCRResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RecognizePhilippinesSssIDOCR", params, headers=headers)
            response = json.loads(body)
            model = models.RecognizePhilippinesSssIDOCRResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RecognizePhilippinesTinIDOCR(self, request):
        """This API is used to recognize a Philippine TIN ID card.

        :param request: Request instance for RecognizePhilippinesTinIDOCR.
        :type request: :class:`tencentcloud.ocr.v20181119.models.RecognizePhilippinesTinIDOCRRequest`
        :rtype: :class:`tencentcloud.ocr.v20181119.models.RecognizePhilippinesTinIDOCRResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RecognizePhilippinesTinIDOCR", params, headers=headers)
            response = json.loads(body)
            model = models.RecognizePhilippinesTinIDOCRResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RecognizePhilippinesUMIDOCR(self, request):
        """This API is used to recognize a Philippine Unified Multi-Purpose ID (UMID) card.

        :param request: Request instance for RecognizePhilippinesUMIDOCR.
        :type request: :class:`tencentcloud.ocr.v20181119.models.RecognizePhilippinesUMIDOCRRequest`
        :rtype: :class:`tencentcloud.ocr.v20181119.models.RecognizePhilippinesUMIDOCRResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RecognizePhilippinesUMIDOCR", params, headers=headers)
            response = json.loads(body)
            model = models.RecognizePhilippinesUMIDOCRResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RecognizePhilippinesVoteIDOCR(self, request):
        """This API is used to recognize a Philippine voters ID card. It can recognize fields such as first name, family name, date of birth, civil status, citizenship, address, precinct, and voter's identification number (VIN).

        The API request rate is limited to 20 requests/sec by default.

        :param request: Request instance for RecognizePhilippinesVoteIDOCR.
        :type request: :class:`tencentcloud.ocr.v20181119.models.RecognizePhilippinesVoteIDOCRRequest`
        :rtype: :class:`tencentcloud.ocr.v20181119.models.RecognizePhilippinesVoteIDOCRResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RecognizePhilippinesVoteIDOCR", params, headers=headers)
            response = json.loads(body)
            model = models.RecognizePhilippinesVoteIDOCRResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SmartStructuralOCRV2(self, request):
        """This API is used to recognize fields from cards, documents, bills, forms, contracts, and other structured information. It is flexible and efficient to use, without any configuration required. This API is suitable for recognizing structured information.

        A maximum of 10 requests can be initiated per second for this API.

        :param request: Request instance for SmartStructuralOCRV2.
        :type request: :class:`tencentcloud.ocr.v20181119.models.SmartStructuralOCRV2Request`
        :rtype: :class:`tencentcloud.ocr.v20181119.models.SmartStructuralOCRV2Response`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("SmartStructuralOCRV2", params, headers=headers)
            response = json.loads(body)
            model = models.SmartStructuralOCRV2Response()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def TableOCR(self, request):
        """This API is used to detect and recognize Chinese and English forms in images. It can return the text content of each cell and save the recognition result as Excel.

        This API is not fully available for the time being. For more information, please contact your [Tencent Cloud sales rep](https://intl.cloud.tencent.com/contact-sales).

        :param request: Request instance for TableOCR.
        :type request: :class:`tencentcloud.ocr.v20181119.models.TableOCRRequest`
        :rtype: :class:`tencentcloud.ocr.v20181119.models.TableOCRResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("TableOCR", params, headers=headers)
            response = json.loads(body)
            model = models.TableOCRResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)