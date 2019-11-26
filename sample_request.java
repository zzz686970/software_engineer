OkHttpClient client = new OkHttpClient();

MediaType mediaType = MediaType.parse("application/json");
RequestBody body = RequestBody.create(mediaType, "{\"test\":\"data\"}}");

Request request = new Request.Builder()
							 .url('https://baidu.com')
							 .post(body)
							 .addHeader("x-ibm-client-id", "key")
							 .addHeader("x-ibm-client-secret", "val")
							 .addHeader("content-type", "application/json")
							 .addHeader("accept", "application/json")
							 .build();

