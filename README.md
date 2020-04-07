TODO: complete the documentation

### _Request_:
* supported build_type: [gradle, maven, sbt]
~~~text
POST: http://localhost:8080/build
Content-Type: application/json
{
    "build_type": "sbt",
    "transactionId": "55a0ec45-ad52-4d53-8674-f8843e44c85e",
    "sourcePath": "D:\\Development\\IntelliJ\\JVMBT\\scala-sbt",
    "fatJarLocation": "D:\\Development\\IntelliJ\\JVMBT\\scala-sbt\\jvmbt\\out\\sbt_fat.jar"
}
~~~

### _Response_:
~~~text
{
    "transactionId": "55a0ec45-ad52-4d53-8674-f8843e44c85e",
    "jar_location": "D:\\Development\\IntelliJ\\JVMBT\\scala-sbt\\jvmbt\\out\\sbt_fat.jar"
}
~~~