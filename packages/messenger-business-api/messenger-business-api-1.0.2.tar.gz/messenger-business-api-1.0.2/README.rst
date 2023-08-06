Messenger Business api
======================

This repository is a wrapper for Meta messenger api for Messenger and
Instagram

Send a message
--------------

.. code:: python

   from messenger-business-apy import MessengerApi

   access_token: "YOUR TOKEN", 
   page_id: "YOUR PAGE ID"  # like ID of page instagram
   api_version: "YOUR PAGE VERSION"  # default v16.0 - OPTIONAL

   messenger = MessengerApi(access_token=access_token,page_id=page_id,api_version=api_version)


   messenger.send_text_message(user_id='291380182300130918', message='This is a test!')

   #ps the user_id is fake only example

Download of file
----------------

.. code:: python

   from messenger-business-apy import MessengerApi

   access_token: 'YOUR TOKEN, 
   page_id: "YOUR PAGE ID"  # like ID of page instagram
   api_version: "YOUR PAGE VERSION"  # default v16.0 - OPTIONAL

   messenger = MessengerApi(access_token=access_token,page_id=page_id,api_version=api_version)

   uri: "URL for downloading media file" 

   messenger.get_media(uri=uri )

