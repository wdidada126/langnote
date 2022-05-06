# yum

yum whatprovides autoconf automake

/etc/yum.repos.d/

vbatts-bazel-epel-7.repo

[copr:copr.fedorainfracloud.org:vbatts:bazel]
name=Copr repo for bazel owned by vbatts
baseurl=https://download.copr.fedorainfracloud.org/results/vbatts/bazel/epel-7-$basearch/
type=rpm-md
skip_if_unavailable=True
gpgcheck=1
gpgkey=https://download.copr.fedorainfracloud.org/results/vbatts/bazel/pubkey.gpg
repo_gpgcheck=0
enabled=1
enabled_metadata=1


腾讯
搭建rpm包管理平台
一般库是最新版





yum list installed



[使用yum查看安装了哪些软件包、某软件包是否已经安装？](https://blog.csdn.net/rentian1/article/details/93768557)



[yum 查看安装的包 包含了哪些文件](https://blog.csdn.net/weixin_38601833/article/details/98628078)

poco-devel
1.6.1

[wdidada@10-23-29-39 ~]$ repoquery -ql poco-devel.x86_64
/usr/include/Poco
/usr/include/Poco/ASCIIEncoding.h
/usr/include/Poco/AbstractCache.h
/usr/include/Poco/AbstractDelegate.h
/usr/include/Poco/AbstractEvent.h
/usr/include/Poco/AbstractObserver.h
/usr/include/Poco/AbstractPriorityDelegate.h
/usr/include/Poco/AbstractStrategy.h
/usr/include/Poco/AccessExpirationDecorator.h
/usr/include/Poco/AccessExpireCache.h
/usr/include/Poco/AccessExpireLRUCache.h
/usr/include/Poco/AccessExpireStrategy.h
/usr/include/Poco/ActiveDispatcher.h
/usr/include/Poco/ActiveMethod.h
/usr/include/Poco/ActiveResult.h
/usr/include/Poco/ActiveRunnable.h
/usr/include/Poco/ActiveStarter.h
/usr/include/Poco/Activity.h
/usr/include/Poco/Alignment.h
/usr/include/Poco/Any.h
/usr/include/Poco/ArchiveStrategy.h
/usr/include/Poco/Array.h
/usr/include/Poco/Ascii.h
/usr/include/Poco/AsyncChannel.h
/usr/include/Poco/AtomicCounter.h
/usr/include/Poco/AutoPtr.h
/usr/include/Poco/AutoReleasePool.h
/usr/include/Poco/Base32Decoder.h
/usr/include/Poco/Base32Encoder.h
/usr/include/Poco/Base64Decoder.h
/usr/include/Poco/Base64Encoder.h
/usr/include/Poco/BasicEvent.h
/usr/include/Poco/BinaryReader.h
/usr/include/Poco/BinaryWriter.h
/usr/include/Poco/Buffer.h
/usr/include/Poco/BufferAllocator.h
/usr/include/Poco/BufferedBidirectionalStreamBuf.h
/usr/include/Poco/BufferedStreamBuf.h
/usr/include/Poco/Bugcheck.h
/usr/include/Poco/ByteOrder.h
/usr/include/Poco/Channel.h
/usr/include/Poco/Checksum.h
/usr/include/Poco/ClassLibrary.h
/usr/include/Poco/ClassLoader.h
/usr/include/Poco/Clock.h
/usr/include/Poco/Condition.h
/usr/include/Poco/Config.h
/usr/include/Poco/Configurable.h
/usr/include/Poco/ConsoleChannel.h
/usr/include/Poco/CountingStream.h
/usr/include/Poco/Crypto
/usr/include/Poco/Crypto/Cipher.h
/usr/include/Poco/Crypto/CipherFactory.h
/usr/include/Poco/Crypto/CipherImpl.h
/usr/include/Poco/Crypto/CipherKey.h
/usr/include/Poco/Crypto/CipherKeyImpl.h
/usr/include/Poco/Crypto/Crypto.h
/usr/include/Poco/Crypto/CryptoStream.h
/usr/include/Poco/Crypto/CryptoTransform.h
/usr/include/Poco/Crypto/DigestEngine.h
/usr/include/Poco/Crypto/OpenSSLInitializer.h
/usr/include/Poco/Crypto/RSACipherImpl.h
/usr/include/Poco/Crypto/RSADigestEngine.h
/usr/include/Poco/Crypto/RSAKey.h
/usr/include/Poco/Crypto/RSAKeyImpl.h
/usr/include/Poco/Crypto/X509Certificate.h
/usr/include/Poco/DOM
/usr/include/Poco/DOM/AbstractContainerNode.h
/usr/include/Poco/DOM/AbstractNode.h
/usr/include/Poco/DOM/Attr.h
/usr/include/Poco/DOM/AttrMap.h
/usr/include/Poco/DOM/AutoPtr.h
/usr/include/Poco/DOM/CDATASection.h
/usr/include/Poco/DOM/CharacterData.h
/usr/include/Poco/DOM/ChildNodesList.h
/usr/include/Poco/DOM/Comment.h
/usr/include/Poco/DOM/DOMBuilder.h
/usr/include/Poco/DOM/DOMException.h
/usr/include/Poco/DOM/DOMImplementation.h
/usr/include/Poco/DOM/DOMObject.h
/usr/include/Poco/DOM/DOMParser.h
/usr/include/Poco/DOM/DOMSerializer.h
/usr/include/Poco/DOM/DOMWriter.h
/usr/include/Poco/DOM/DTDMap.h
/usr/include/Poco/DOM/Document.h
/usr/include/Poco/DOM/DocumentEvent.h
/usr/include/Poco/DOM/DocumentFragment.h
/usr/include/Poco/DOM/DocumentType.h
/usr/include/Poco/DOM/Element.h
/usr/include/Poco/DOM/ElementsByTagNameList.h
/usr/include/Poco/DOM/Entity.h
/usr/include/Poco/DOM/EntityReference.h
/usr/include/Poco/DOM/Event.h
/usr/include/Poco/DOM/EventDispatcher.h
/usr/include/Poco/DOM/EventException.h
/usr/include/Poco/DOM/EventListener.h
/usr/include/Poco/DOM/EventTarget.h
/usr/include/Poco/DOM/MutationEvent.h
/usr/include/Poco/DOM/NamedNodeMap.h
/usr/include/Poco/DOM/Node.h
/usr/include/Poco/DOM/NodeAppender.h
/usr/include/Poco/DOM/NodeFilter.h
/usr/include/Poco/DOM/NodeIterator.h
/usr/include/Poco/DOM/NodeList.h
/usr/include/Poco/DOM/Notation.h
/usr/include/Poco/DOM/ProcessingInstruction.h
/usr/include/Poco/DOM/Text.h
/usr/include/Poco/DOM/TreeWalker.h
/usr/include/Poco/Data
/usr/include/Poco/Data/AbstractBinder.h
/usr/include/Poco/Data/AbstractBinding.h
/usr/include/Poco/Data/AbstractExtraction.h
/usr/include/Poco/Data/AbstractExtractor.h
/usr/include/Poco/Data/AbstractPreparation.h
/usr/include/Poco/Data/AbstractPreparator.h
/usr/include/Poco/Data/AbstractSessionImpl.h
/usr/include/Poco/Data/ArchiveStrategy.h
/usr/include/Poco/Data/AutoTransaction.h
/usr/include/Poco/Data/Binding.h
/usr/include/Poco/Data/Bulk.h
/usr/include/Poco/Data/BulkBinding.h
/usr/include/Poco/Data/BulkExtraction.h
/usr/include/Poco/Data/Column.h
/usr/include/Poco/Data/Connector.h
/usr/include/Poco/Data/Constants.h
/usr/include/Poco/Data/Data.h
/usr/include/Poco/Data/DataException.h
/usr/include/Poco/Data/Date.h
/usr/include/Poco/Data/DynamicDateTime.h
/usr/include/Poco/Data/DynamicLOB.h
/usr/include/Poco/Data/Extraction.h
/usr/include/Poco/Data/LOB.h
/usr/include/Poco/Data/LOBStream.h
/usr/include/Poco/Data/Limit.h
/usr/include/Poco/Data/MetaColumn.h
/usr/include/Poco/Data/MySQL
/usr/include/Poco/Data/MySQL/Binder.h
/usr/include/Poco/Data/MySQL/Connector.h
/usr/include/Poco/Data/MySQL/Extractor.h
/usr/include/Poco/Data/MySQL/MySQL.h
/usr/include/Poco/Data/MySQL/MySQLException.h
/usr/include/Poco/Data/MySQL/MySQLStatementImpl.h
/usr/include/Poco/Data/MySQL/ResultMetadata.h
/usr/include/Poco/Data/MySQL/SessionHandle.h
/usr/include/Poco/Data/MySQL/SessionImpl.h
/usr/include/Poco/Data/MySQL/StatementExecutor.h
/usr/include/Poco/Data/MySQL/Utility.h
/usr/include/Poco/Data/ODBC
/usr/include/Poco/Data/ODBC/Binder.h
/usr/include/Poco/Data/ODBC/ConnectionHandle.h
/usr/include/Poco/Data/ODBC/Connector.h
/usr/include/Poco/Data/ODBC/Diagnostics.h
/usr/include/Poco/Data/ODBC/EnvironmentHandle.h
/usr/include/Poco/Data/ODBC/Error.h
/usr/include/Poco/Data/ODBC/Extractor.h
/usr/include/Poco/Data/ODBC/Handle.h
/usr/include/Poco/Data/ODBC/ODBC.h
/usr/include/Poco/Data/ODBC/ODBCException.h
/usr/include/Poco/Data/ODBC/ODBCMetaColumn.h
/usr/include/Poco/Data/ODBC/ODBCStatementImpl.h
/usr/include/Poco/Data/ODBC/Parameter.h
/usr/include/Poco/Data/ODBC/Preparator.h
/usr/include/Poco/Data/ODBC/SessionImpl.h
/usr/include/Poco/Data/ODBC/TypeInfo.h
/usr/include/Poco/Data/ODBC/Unicode.h
/usr/include/Poco/Data/ODBC/Unicode_UNIXODBC.h
/usr/include/Poco/Data/ODBC/Unicode_WIN32.h
/usr/include/Poco/Data/ODBC/Utility.h
/usr/include/Poco/Data/PooledSessionHolder.h
/usr/include/Poco/Data/PooledSessionImpl.h
/usr/include/Poco/Data/Position.h
/usr/include/Poco/Data/Preparation.h
/usr/include/Poco/Data/Range.h
/usr/include/Poco/Data/RecordSet.h
/usr/include/Poco/Data/Row.h
/usr/include/Poco/Data/RowFilter.h
/usr/include/Poco/Data/RowFormatter.h
/usr/include/Poco/Data/RowIterator.h
/usr/include/Poco/Data/SQLChannel.h
/usr/include/Poco/Data/SQLite
/usr/include/Poco/Data/SQLite/Binder.h
/usr/include/Poco/Data/SQLite/Connector.h
/usr/include/Poco/Data/SQLite/Extractor.h
/usr/include/Poco/Data/SQLite/Notifier.h
/usr/include/Poco/Data/SQLite/SQLite.h
/usr/include/Poco/Data/SQLite/SQLiteException.h
/usr/include/Poco/Data/SQLite/SQLiteStatementImpl.h
/usr/include/Poco/Data/SQLite/SessionImpl.h
/usr/include/Poco/Data/SQLite/Utility.h
/usr/include/Poco/Data/Session.h
/usr/include/Poco/Data/SessionFactory.h
/usr/include/Poco/Data/SessionImpl.h
/usr/include/Poco/Data/SessionPool.h
/usr/include/Poco/Data/SessionPoolContainer.h
/usr/include/Poco/Data/SimpleRowFormatter.h
/usr/include/Poco/Data/Statement.h
/usr/include/Poco/Data/StatementCreator.h
/usr/include/Poco/Data/StatementImpl.h
/usr/include/Poco/Data/Time.h
/usr/include/Poco/Data/Transaction.h
/usr/include/Poco/Data/TypeHandler.h
/usr/include/Poco/DateTime.h
/usr/include/Poco/DateTimeFormat.h
/usr/include/Poco/DateTimeFormatter.h
/usr/include/Poco/DateTimeParser.h
/usr/include/Poco/Debugger.h
/usr/include/Poco/DefaultStrategy.h
/usr/include/Poco/DeflatingStream.h
/usr/include/Poco/Delegate.h
/usr/include/Poco/DigestEngine.h
/usr/include/Poco/DigestStream.h
/usr/include/Poco/DirectoryIterator.h
/usr/include/Poco/DirectoryIteratorStrategy.h
/usr/include/Poco/DirectoryIterator_UNIX.h
/usr/include/Poco/DirectoryIterator_VMS.h
/usr/include/Poco/DirectoryIterator_WIN32.h
/usr/include/Poco/DirectoryIterator_WIN32U.h
/usr/include/Poco/DirectoryWatcher.h
/usr/include/Poco/Dynamic
/usr/include/Poco/Dynamic/Pair.h
/usr/include/Poco/Dynamic/Struct.h
/usr/include/Poco/Dynamic/Var.h
/usr/include/Poco/Dynamic/VarHolder.h
/usr/include/Poco/Dynamic/VarIterator.h
/usr/include/Poco/DynamicAny.h
/usr/include/Poco/DynamicAnyHolder.h
/usr/include/Poco/DynamicFactory.h
/usr/include/Poco/DynamicStruct.h
/usr/include/Poco/Environment.h
/usr/include/Poco/Environment_UNIX.h
/usr/include/Poco/Environment_VMS.h
/usr/include/Poco/Environment_VX.h
/usr/include/Poco/Environment_WIN32.h
/usr/include/Poco/Environment_WIN32U.h
/usr/include/Poco/Environment_WINCE.h
/usr/include/Poco/Error.h
/usr/include/Poco/ErrorHandler.h
/usr/include/Poco/Event.h
/usr/include/Poco/EventArgs.h
/usr/include/Poco/EventLogChannel.h
/usr/include/Poco/Event_POSIX.h
/usr/include/Poco/Event_VX.h
/usr/include/Poco/Event_WIN32.h
/usr/include/Poco/Exception.h
/usr/include/Poco/ExpirationDecorator.h
/usr/include/Poco/Expire.h
/usr/include/Poco/ExpireCache.h
/usr/include/Poco/ExpireLRUCache.h
/usr/include/Poco/ExpireStrategy.h
/usr/include/Poco/FIFOBuffer.h
/usr/include/Poco/FIFOBufferStream.h
/usr/include/Poco/FIFOEvent.h
/usr/include/Poco/FIFOStrategy.h
/usr/include/Poco/FPEnvironment.h
/usr/include/Poco/FPEnvironment_C99.h
/usr/include/Poco/FPEnvironment_DEC.h
/usr/include/Poco/FPEnvironment_DUMMY.h
/usr/include/Poco/FPEnvironment_SUN.h
/usr/include/Poco/FPEnvironment_WIN32.h
/usr/include/Poco/File.h
/usr/include/Poco/FileChannel.h
/usr/include/Poco/FileStream.h
/usr/include/Poco/FileStreamFactory.h
/usr/include/Poco/FileStream_POSIX.h
/usr/include/Poco/FileStream_WIN32.h
/usr/include/Poco/File_UNIX.h
/usr/include/Poco/File_VMS.h
/usr/include/Poco/File_VX.h
/usr/include/Poco/File_WIN32.h
/usr/include/Poco/File_WIN32U.h
/usr/include/Poco/File_WINCE.h
/usr/include/Poco/Format.h
/usr/include/Poco/Formatter.h
/usr/include/Poco/FormattingChannel.h
/usr/include/Poco/Foundation.h
/usr/include/Poco/FunctionDelegate.h
/usr/include/Poco/FunctionPriorityDelegate.h
/usr/include/Poco/Glob.h
/usr/include/Poco/HMACEngine.h
/usr/include/Poco/Hash.h
/usr/include/Poco/HashFunction.h
/usr/include/Poco/HashMap.h
/usr/include/Poco/HashSet.h
/usr/include/Poco/HashStatistic.h
/usr/include/Poco/HashTable.h
/usr/include/Poco/HexBinaryDecoder.h
/usr/include/Poco/HexBinaryEncoder.h
/usr/include/Poco/InflatingStream.h
/usr/include/Poco/Instantiator.h
/usr/include/Poco/JSON
/usr/include/Poco/JSON/Array.h
/usr/include/Poco/JSON/Handler.h
/usr/include/Poco/JSON/JSON.h
/usr/include/Poco/JSON/JSONException.h
/usr/include/Poco/JSON/Object.h
/usr/include/Poco/JSON/ParseHandler.h
/usr/include/Poco/JSON/Parser.h
/usr/include/Poco/JSON/PrintHandler.h
/usr/include/Poco/JSON/Query.h
/usr/include/Poco/JSON/Stringifier.h
/usr/include/Poco/JSON/Template.h
/usr/include/Poco/JSON/TemplateCache.h
/usr/include/Poco/KeyValueArgs.h
/usr/include/Poco/LRUCache.h
/usr/include/Poco/LRUStrategy.h
/usr/include/Poco/Latin1Encoding.h
/usr/include/Poco/Latin2Encoding.h
/usr/include/Poco/Latin9Encoding.h
/usr/include/Poco/LineEndingConverter.h
/usr/include/Poco/LinearHashTable.h
/usr/include/Poco/ListMap.h
/usr/include/Poco/LocalDateTime.h
/usr/include/Poco/LogFile.h
/usr/include/Poco/LogFile_STD.h
/usr/include/Poco/LogFile_VMS.h
/usr/include/Poco/LogFile_WIN32.h
/usr/include/Poco/LogFile_WIN32U.h
/usr/include/Poco/LogStream.h
/usr/include/Poco/Logger.h
/usr/include/Poco/LoggingFactory.h
/usr/include/Poco/LoggingRegistry.h
/usr/include/Poco/MD4Engine.h
/usr/include/Poco/MD5Engine.h
/usr/include/Poco/Manifest.h
/usr/include/Poco/MemoryPool.h
/usr/include/Poco/MemoryStream.h
/usr/include/Poco/Message.h
/usr/include/Poco/MetaObject.h
/usr/include/Poco/MetaProgramming.h
/usr/include/Poco/MongoDB
/usr/include/Poco/MongoDB/Array.h
/usr/include/Poco/MongoDB/BSONReader.h
/usr/include/Poco/MongoDB/BSONWriter.h
/usr/include/Poco/MongoDB/Binary.h
/usr/include/Poco/MongoDB/Connection.h
/usr/include/Poco/MongoDB/Cursor.h
/usr/include/Poco/MongoDB/Database.h
/usr/include/Poco/MongoDB/DeleteRequest.h
/usr/include/Poco/MongoDB/Document.h
/usr/include/Poco/MongoDB/Element.h
/usr/include/Poco/MongoDB/GetMoreRequest.h
/usr/include/Poco/MongoDB/InsertRequest.h
/usr/include/Poco/MongoDB/JavaScriptCode.h
/usr/include/Poco/MongoDB/KillCursorsRequest.h
/usr/include/Poco/MongoDB/Message.h
/usr/include/Poco/MongoDB/MessageHeader.h
/usr/include/Poco/MongoDB/MongoDB.h
/usr/include/Poco/MongoDB/ObjectId.h
/usr/include/Poco/MongoDB/PoolableConnectionFactory.h
/usr/include/Poco/MongoDB/QueryRequest.h
/usr/include/Poco/MongoDB/RegularExpression.h
/usr/include/Poco/MongoDB/ReplicaSet.h
/usr/include/Poco/MongoDB/RequestMessage.h
/usr/include/Poco/MongoDB/ResponseMessage.h
/usr/include/Poco/MongoDB/UpdateRequest.h
/usr/include/Poco/Mutex.h
/usr/include/Poco/Mutex_POSIX.h
/usr/include/Poco/Mutex_VX.h
/usr/include/Poco/Mutex_WIN32.h
/usr/include/Poco/Mutex_WINCE.h
/usr/include/Poco/NObserver.h
/usr/include/Poco/NamedEvent.h
/usr/include/Poco/NamedEvent_Android.h
/usr/include/Poco/NamedEvent_UNIX.h
/usr/include/Poco/NamedEvent_VMS.h
/usr/include/Poco/NamedEvent_WIN32.h
/usr/include/Poco/NamedEvent_WIN32U.h
/usr/include/Poco/NamedMutex.h
/usr/include/Poco/NamedMutex_Android.h
/usr/include/Poco/NamedMutex_UNIX.h
/usr/include/Poco/NamedMutex_VMS.h
/usr/include/Poco/NamedMutex_WIN32.h
/usr/include/Poco/NamedMutex_WIN32U.h
/usr/include/Poco/NamedTuple.h
/usr/include/Poco/NestedDiagnosticContext.h
/usr/include/Poco/Net
/usr/include/Poco/Net/AbstractHTTPRequestHandler.h
/usr/include/Poco/Net/AcceptCertificateHandler.h
/usr/include/Poco/Net/CertificateHandlerFactory.h
/usr/include/Poco/Net/CertificateHandlerFactoryMgr.h
/usr/include/Poco/Net/ConsoleCertificateHandler.h
/usr/include/Poco/Net/Context.h
/usr/include/Poco/Net/DNS.h
/usr/include/Poco/Net/DatagramSocket.h
/usr/include/Poco/Net/DatagramSocketImpl.h
/usr/include/Poco/Net/DialogSocket.h
/usr/include/Poco/Net/FTPClientSession.h
/usr/include/Poco/Net/FTPStreamFactory.h
/usr/include/Poco/Net/FilePartSource.h
/usr/include/Poco/Net/HTMLForm.h
/usr/include/Poco/Net/HTTPAuthenticationParams.h
/usr/include/Poco/Net/HTTPBasicCredentials.h
/usr/include/Poco/Net/HTTPBasicStreamBuf.h
/usr/include/Poco/Net/HTTPBufferAllocator.h
/usr/include/Poco/Net/HTTPChunkedStream.h
/usr/include/Poco/Net/HTTPClientSession.h
/usr/include/Poco/Net/HTTPCookie.h
/usr/include/Poco/Net/HTTPCredentials.h
/usr/include/Poco/Net/HTTPDigestCredentials.h
/usr/include/Poco/Net/HTTPFixedLengthStream.h
/usr/include/Poco/Net/HTTPHeaderStream.h
/usr/include/Poco/Net/HTTPIOStream.h
/usr/include/Poco/Net/HTTPMessage.h
/usr/include/Poco/Net/HTTPRequest.h
/usr/include/Poco/Net/HTTPRequestHandler.h
/usr/include/Poco/Net/HTTPRequestHandlerFactory.h
/usr/include/Poco/Net/HTTPResponse.h
/usr/include/Poco/Net/HTTPSClientSession.h
/usr/include/Poco/Net/HTTPSSessionInstantiator.h
/usr/include/Poco/Net/HTTPSStreamFactory.h
/usr/include/Poco/Net/HTTPServer.h
/usr/include/Poco/Net/HTTPServerConnection.h
/usr/include/Poco/Net/HTTPServerConnectionFactory.h
/usr/include/Poco/Net/HTTPServerParams.h
/usr/include/Poco/Net/HTTPServerRequest.h
/usr/include/Poco/Net/HTTPServerRequestImpl.h
/usr/include/Poco/Net/HTTPServerResponse.h
/usr/include/Poco/Net/HTTPServerResponseImpl.h
/usr/include/Poco/Net/HTTPServerSession.h
/usr/include/Poco/Net/HTTPSession.h
/usr/include/Poco/Net/HTTPSessionFactory.h
/usr/include/Poco/Net/HTTPSessionInstantiator.h
/usr/include/Poco/Net/HTTPStream.h
/usr/include/Poco/Net/HTTPStreamFactory.h
/usr/include/Poco/Net/HostEntry.h
/usr/include/Poco/Net/ICMPClient.h
/usr/include/Poco/Net/ICMPEventArgs.h
/usr/include/Poco/Net/ICMPPacket.h
/usr/include/Poco/Net/ICMPPacketImpl.h
/usr/include/Poco/Net/ICMPSocket.h
/usr/include/Poco/Net/ICMPSocketImpl.h
/usr/include/Poco/Net/ICMPv4PacketImpl.h
/usr/include/Poco/Net/IPAddress.h
/usr/include/Poco/Net/IPAddressImpl.h
/usr/include/Poco/Net/InvalidCertificateHandler.h
/usr/include/Poco/Net/KeyConsoleHandler.h
/usr/include/Poco/Net/KeyFileHandler.h
/usr/include/Poco/Net/MailMessage.h
/usr/include/Poco/Net/MailRecipient.h
/usr/include/Poco/Net/MailStream.h
/usr/include/Poco/Net/MediaType.h
/usr/include/Poco/Net/MessageHeader.h
/usr/include/Poco/Net/MulticastSocket.h
/usr/include/Poco/Net/MultipartReader.h
/usr/include/Poco/Net/MultipartWriter.h
/usr/include/Poco/Net/NTPClient.h
/usr/include/Poco/Net/NTPEventArgs.h
/usr/include/Poco/Net/NTPPacket.h
/usr/include/Poco/Net/NameValueCollection.h
/usr/include/Poco/Net/Net.h
/usr/include/Poco/Net/NetException.h
/usr/include/Poco/Net/NetSSL.h
/usr/include/Poco/Net/NetworkInterface.h
/usr/include/Poco/Net/NullPartHandler.h
/usr/include/Poco/Net/OAuth10Credentials.h
/usr/include/Poco/Net/OAuth20Credentials.h
/usr/include/Poco/Net/POP3ClientSession.h
/usr/include/Poco/Net/ParallelSocketAcceptor.h
/usr/include/Poco/Net/ParallelSocketReactor.h
/usr/include/Poco/Net/PartHandler.h
/usr/include/Poco/Net/PartSource.h
/usr/include/Poco/Net/PartStore.h
/usr/include/Poco/Net/PrivateKeyFactory.h
/usr/include/Poco/Net/PrivateKeyFactoryMgr.h
/usr/include/Poco/Net/PrivateKeyPassphraseHandler.h
/usr/include/Poco/Net/QuotedPrintableDecoder.h
/usr/include/Poco/Net/QuotedPrintableEncoder.h
/usr/include/Poco/Net/RawSocket.h
/usr/include/Poco/Net/RawSocketImpl.h
/usr/include/Poco/Net/RejectCertificateHandler.h
/usr/include/Poco/Net/RemoteSyslogChannel.h
/usr/include/Poco/Net/RemoteSyslogListener.h
/usr/include/Poco/Net/SMTPChannel.h
/usr/include/Poco/Net/SMTPClientSession.h
/usr/include/Poco/Net/SSLException.h
/usr/include/Poco/Net/SSLManager.h
/usr/include/Poco/Net/SecureSMTPClientSession.h
/usr/include/Poco/Net/SecureServerSocket.h
/usr/include/Poco/Net/SecureServerSocketImpl.h
/usr/include/Poco/Net/SecureSocketImpl.h
/usr/include/Poco/Net/SecureStreamSocket.h
/usr/include/Poco/Net/SecureStreamSocketImpl.h
/usr/include/Poco/Net/ServerSocket.h
/usr/include/Poco/Net/ServerSocketImpl.h
/usr/include/Poco/Net/Session.h
/usr/include/Poco/Net/Socket.h
/usr/include/Poco/Net/SocketAcceptor.h
/usr/include/Poco/Net/SocketAddress.h
/usr/include/Poco/Net/SocketAddressImpl.h
/usr/include/Poco/Net/SocketConnector.h
/usr/include/Poco/Net/SocketDefs.h
/usr/include/Poco/Net/SocketImpl.h
/usr/include/Poco/Net/SocketNotification.h
/usr/include/Poco/Net/SocketNotifier.h
/usr/include/Poco/Net/SocketReactor.h
/usr/include/Poco/Net/SocketStream.h
/usr/include/Poco/Net/StreamSocket.h
/usr/include/Poco/Net/StreamSocketImpl.h
/usr/include/Poco/Net/StringPartSource.h
/usr/include/Poco/Net/TCPServer.h
/usr/include/Poco/Net/TCPServerConnection.h
/usr/include/Poco/Net/TCPServerConnectionFactory.h
/usr/include/Poco/Net/TCPServerDispatcher.h
/usr/include/Poco/Net/TCPServerParams.h
/usr/include/Poco/Net/Utility.h
/usr/include/Poco/Net/VerificationErrorArgs.h
/usr/include/Poco/Net/WebSocket.h
/usr/include/Poco/Net/WebSocketImpl.h
/usr/include/Poco/Net/X509Certificate.h
/usr/include/Poco/Notification.h
/usr/include/Poco/NotificationCenter.h
/usr/include/Poco/NotificationQueue.h
/usr/include/Poco/NotificationStrategy.h
/usr/include/Poco/NullChannel.h
/usr/include/Poco/NullStream.h
/usr/include/Poco/Nullable.h
/usr/include/Poco/NumberFormatter.h
/usr/include/Poco/NumberParser.h
/usr/include/Poco/NumericString.h
/usr/include/Poco/ObjectPool.h
/usr/include/Poco/Observer.h
/usr/include/Poco/OpcomChannel.h
/usr/include/Poco/Optional.h
/usr/include/Poco/PBKDF2Engine.h
/usr/include/Poco/Path.h
/usr/include/Poco/Path_UNIX.h
/usr/include/Poco/Path_VMS.h
/usr/include/Poco/Path_WIN32.h
/usr/include/Poco/Path_WIN32U.h
/usr/include/Poco/Path_WINCE.h
/usr/include/Poco/PatternFormatter.h
/usr/include/Poco/Pipe.h
/usr/include/Poco/PipeImpl.h
/usr/include/Poco/PipeImpl_DUMMY.h
/usr/include/Poco/PipeImpl_POSIX.h
/usr/include/Poco/PipeImpl_WIN32.h
/usr/include/Poco/PipeStream.h
/usr/include/Poco/Platform.h
/usr/include/Poco/Platform_POSIX.h
/usr/include/Poco/Platform_VMS.h
/usr/include/Poco/Platform_VX.h
/usr/include/Poco/Platform_WIN32.h
/usr/include/Poco/Poco.h
/usr/include/Poco/PriorityDelegate.h
/usr/include/Poco/PriorityEvent.h
/usr/include/Poco/PriorityExpire.h
/usr/include/Poco/PriorityNotificationQueue.h
/usr/include/Poco/PriorityStrategy.h
/usr/include/Poco/Process.h
/usr/include/Poco/Process_UNIX.h
/usr/include/Poco/Process_VMS.h
/usr/include/Poco/Process_VX.h
/usr/include/Poco/Process_WIN32.h
/usr/include/Poco/Process_WIN32U.h
/usr/include/Poco/Process_WINCE.h
/usr/include/Poco/PurgeStrategy.h
/usr/include/Poco/RWLock.h
/usr/include/Poco/RWLock_Android.h
/usr/include/Poco/RWLock_POSIX.h
/usr/include/Poco/RWLock_VX.h
/usr/include/Poco/RWLock_WIN32.h
/usr/include/Poco/RWLock_WINCE.h
/usr/include/Poco/Random.h
/usr/include/Poco/RandomStream.h
/usr/include/Poco/RecursiveDirectoryIterator.h
/usr/include/Poco/RecursiveDirectoryIteratorImpl.h
/usr/include/Poco/RefCountedObject.h
/usr/include/Poco/RegularExpression.h
/usr/include/Poco/RotateStrategy.h
/usr/include/Poco/Runnable.h
/usr/include/Poco/RunnableAdapter.h
/usr/include/Poco/SAX
/usr/include/Poco/SAX/Attributes.h
/usr/include/Poco/SAX/AttributesImpl.h
/usr/include/Poco/SAX/ContentHandler.h
/usr/include/Poco/SAX/DTDHandler.h
/usr/include/Poco/SAX/DeclHandler.h
/usr/include/Poco/SAX/DefaultHandler.h
/usr/include/Poco/SAX/EntityResolver.h
/usr/include/Poco/SAX/EntityResolverImpl.h
/usr/include/Poco/SAX/ErrorHandler.h
/usr/include/Poco/SAX/InputSource.h
/usr/include/Poco/SAX/LexicalHandler.h
/usr/include/Poco/SAX/Locator.h
/usr/include/Poco/SAX/LocatorImpl.h
/usr/include/Poco/SAX/NamespaceSupport.h
/usr/include/Poco/SAX/SAXException.h
/usr/include/Poco/SAX/SAXParser.h
/usr/include/Poco/SAX/WhitespaceFilter.h
/usr/include/Poco/SAX/XMLFilter.h
/usr/include/Poco/SAX/XMLFilterImpl.h
/usr/include/Poco/SAX/XMLReader.h
/usr/include/Poco/SHA1Engine.h
/usr/include/Poco/ScopedLock.h
/usr/include/Poco/ScopedUnlock.h
/usr/include/Poco/Semaphore.h
/usr/include/Poco/Semaphore_POSIX.h
/usr/include/Poco/Semaphore_VX.h
/usr/include/Poco/Semaphore_WIN32.h
/usr/include/Poco/SharedLibrary.h
/usr/include/Poco/SharedLibrary_HPUX.h
/usr/include/Poco/SharedLibrary_UNIX.h
/usr/include/Poco/SharedLibrary_VMS.h
/usr/include/Poco/SharedLibrary_VX.h
/usr/include/Poco/SharedLibrary_WIN32.h
/usr/include/Poco/SharedLibrary_WIN32U.h
/usr/include/Poco/SharedMemory.h
/usr/include/Poco/SharedMemory_DUMMY.h
/usr/include/Poco/SharedMemory_POSIX.h
/usr/include/Poco/SharedMemory_WIN32.h
/usr/include/Poco/SharedPtr.h
/usr/include/Poco/SignalHandler.h
/usr/include/Poco/SimpleFileChannel.h
/usr/include/Poco/SimpleHashTable.h
/usr/include/Poco/SingletonHolder.h
/usr/include/Poco/SortedDirectoryIterator.h
/usr/include/Poco/SplitterChannel.h
/usr/include/Poco/Stopwatch.h
/usr/include/Poco/StrategyCollection.h
/usr/include/Poco/StreamChannel.h
/usr/include/Poco/StreamConverter.h
/usr/include/Poco/StreamCopier.h
/usr/include/Poco/StreamTokenizer.h
/usr/include/Poco/StreamUtil.h
/usr/include/Poco/String.h
/usr/include/Poco/StringTokenizer.h
/usr/include/Poco/SynchronizedObject.h
/usr/include/Poco/SyslogChannel.h
/usr/include/Poco/Task.h
/usr/include/Poco/TaskManager.h
/usr/include/Poco/TaskNotification.h
/usr/include/Poco/TeeStream.h
/usr/include/Poco/TemporaryFile.h
/usr/include/Poco/TextBufferIterator.h
/usr/include/Poco/TextConverter.h
/usr/include/Poco/TextEncoding.h
/usr/include/Poco/TextIterator.h
/usr/include/Poco/Thread.h
/usr/include/Poco/ThreadLocal.h
/usr/include/Poco/ThreadPool.h
/usr/include/Poco/ThreadTarget.h
/usr/include/Poco/Thread_POSIX.h
/usr/include/Poco/Thread_VX.h
/usr/include/Poco/Thread_WIN32.h
/usr/include/Poco/Thread_WINCE.h
/usr/include/Poco/TimedNotificationQueue.h
/usr/include/Poco/Timer.h
/usr/include/Poco/Timespan.h
/usr/include/Poco/Timestamp.h
/usr/include/Poco/Timezone.h
/usr/include/Poco/Token.h
/usr/include/Poco/Tuple.h
/usr/include/Poco/TypeList.h
/usr/include/Poco/Types.h
/usr/include/Poco/URI.h
/usr/include/Poco/URIStreamFactory.h
/usr/include/Poco/URIStreamOpener.h
/usr/include/Poco/UTF16Encoding.h
/usr/include/Poco/UTF32Encoding.h
/usr/include/Poco/UTF8Encoding.h
/usr/include/Poco/UTF8String.h
/usr/include/Poco/UTFString.h
/usr/include/Poco/UUID.h
/usr/include/Poco/UUIDGenerator.h
/usr/include/Poco/UnWindows.h
/usr/include/Poco/UnbufferedStreamBuf.h
/usr/include/Poco/Unicode.h
/usr/include/Poco/UnicodeConverter.h
/usr/include/Poco/UniqueAccessExpireCache.h
/usr/include/Poco/UniqueAccessExpireLRUCache.h
/usr/include/Poco/UniqueAccessExpireStrategy.h
/usr/include/Poco/UniqueExpireCache.h
/usr/include/Poco/UniqueExpireLRUCache.h
/usr/include/Poco/UniqueExpireStrategy.h
/usr/include/Poco/Util
/usr/include/Poco/Util/AbstractConfiguration.h
/usr/include/Poco/Util/Application.h
/usr/include/Poco/Util/ConfigurationMapper.h
/usr/include/Poco/Util/ConfigurationView.h
/usr/include/Poco/Util/FilesystemConfiguration.h
/usr/include/Poco/Util/HelpFormatter.h
/usr/include/Poco/Util/IniFileConfiguration.h
/usr/include/Poco/Util/IntValidator.h
/usr/include/Poco/Util/JSONConfiguration.h
/usr/include/Poco/Util/LayeredConfiguration.h
/usr/include/Poco/Util/LoggingConfigurator.h
/usr/include/Poco/Util/LoggingSubsystem.h
/usr/include/Poco/Util/MapConfiguration.h
/usr/include/Poco/Util/Option.h
/usr/include/Poco/Util/OptionCallback.h
/usr/include/Poco/Util/OptionException.h
/usr/include/Poco/Util/OptionProcessor.h
/usr/include/Poco/Util/OptionSet.h
/usr/include/Poco/Util/PropertyFileConfiguration.h
/usr/include/Poco/Util/RegExpValidator.h
/usr/include/Poco/Util/ServerApplication.h
/usr/include/Poco/Util/Subsystem.h
/usr/include/Poco/Util/SystemConfiguration.h
/usr/include/Poco/Util/Timer.h
/usr/include/Poco/Util/TimerTask.h
/usr/include/Poco/Util/TimerTaskAdapter.h
/usr/include/Poco/Util/Units.h
/usr/include/Poco/Util/Util.h
/usr/include/Poco/Util/Validator.h
/usr/include/Poco/Util/WinRegistryConfiguration.h
/usr/include/Poco/Util/WinRegistryKey.h
/usr/include/Poco/Util/WinService.h
/usr/include/Poco/Util/XMLConfiguration.h
/usr/include/Poco/ValidArgs.h
/usr/include/Poco/Version.h
/usr/include/Poco/Void.h
/usr/include/Poco/Windows1250Encoding.h
/usr/include/Poco/Windows1251Encoding.h
/usr/include/Poco/Windows1252Encoding.h
/usr/include/Poco/WindowsConsoleChannel.h
/usr/include/Poco/XML
/usr/include/Poco/XML/Name.h
/usr/include/Poco/XML/NamePool.h
/usr/include/Poco/XML/NamespaceStrategy.h
/usr/include/Poco/XML/ParserEngine.h
/usr/include/Poco/XML/XML.h
/usr/include/Poco/XML/XMLException.h
/usr/include/Poco/XML/XMLStream.h
/usr/include/Poco/XML/XMLString.h
/usr/include/Poco/XML/XMLWriter.h
/usr/include/Poco/Zip
/usr/include/Poco/Zip/Add.h
/usr/include/Poco/Zip/AutoDetectStream.h
/usr/include/Poco/Zip/Compress.h
/usr/include/Poco/Zip/Decompress.h
/usr/include/Poco/Zip/Delete.h
/usr/include/Poco/Zip/Keep.h
/usr/include/Poco/Zip/ParseCallback.h
/usr/include/Poco/Zip/PartialStream.h
/usr/include/Poco/Zip/Rename.h
/usr/include/Poco/Zip/Replace.h
/usr/include/Poco/Zip/SkipCallback.h
/usr/include/Poco/Zip/Zip.h
/usr/include/Poco/Zip/ZipArchive.h
/usr/include/Poco/Zip/ZipArchiveInfo.h
/usr/include/Poco/Zip/ZipCommon.h
/usr/include/Poco/Zip/ZipDataInfo.h
/usr/include/Poco/Zip/ZipException.h
/usr/include/Poco/Zip/ZipFileInfo.h
/usr/include/Poco/Zip/ZipLocalFileHeader.h
/usr/include/Poco/Zip/ZipManipulator.h
/usr/include/Poco/Zip/ZipOperation.h
/usr/include/Poco/Zip/ZipStream.h
/usr/include/Poco/Zip/ZipUtil.h
/usr/lib64/libPocoCrypto.so
/usr/lib64/libPocoCryptod.so
/usr/lib64/libPocoData.so
/usr/lib64/libPocoDataMySQL.so
/usr/lib64/libPocoDataMySQLd.so
/usr/lib64/libPocoDataODBC.so
/usr/lib64/libPocoDataODBCd.so
/usr/lib64/libPocoDataSQLite.so
/usr/lib64/libPocoDataSQLited.so
/usr/lib64/libPocoDatad.so
/usr/lib64/libPocoFoundation.so
/usr/lib64/libPocoFoundationd.so
/usr/lib64/libPocoJSON.so
/usr/lib64/libPocoJSONd.so
/usr/lib64/libPocoMongoDB.so
/usr/lib64/libPocoMongoDBd.so
/usr/lib64/libPocoNet.so
/usr/lib64/libPocoNetSSL.so
/usr/lib64/libPocoNetSSLd.so
/usr/lib64/libPocoNetd.so
/usr/lib64/libPocoUtil.so
/usr/lib64/libPocoUtild.so
/usr/lib64/libPocoXML.so
/usr/lib64/libPocoXMLd.so
/usr/lib64/libPocoZip.so
/usr/lib64/libPocoZipd.so

yum -y install libstdc++-4.8.5-28.el7.x86_64
https://www.cnblogs.com/effortsing/p/10363921.html
原因及办法：我第一次安装成了el8的mysql-server，卸载之后，yum没有clean。
1、yum update （可选）
2、rpm -qa|grep mysql #找到已装的rpm包名
3、rpm -e 包名 #卸载
4、yum clean all #清缓存 关键！！
————————————————
版权声明：本文为CSDN博主「柴神」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/chaishen10000/article/details/105967163

`yum info clang`
`yum repolist`

yum --enablerepo=remi install redis -y

```
yum whatprovides libmysqlclient*
```

http://www.cocoachina.com/articles/63213





/var/cache/yum/x86_64/7/ rpm文件缓存


yum 自动安装依赖


yum install createrepo yum-utils -y

Package createrepo-0.9.9-28.el7.noarch already installed and latest version
Package yum-utils-1.1.31-54.el7_8.noarch already installed and latest version


yumdownloader - download RPM packages from Yum repositories
createrepo - Create repomd (xml-rpm-metadata) repository


搭建私有YUM仓库与内网镜像站
https://www.sohu.com/a/333246091_99923293



$ sudo yum-config-manager --add-repo=https://copr.fedorainfracloud.org/coprs/carlwgeorge/ripgrep/repo/epel-7/carlwgeorge-ripgrep-epel-7.repo
$ sudo yum install ripgrep


CentOS7 配置阿里云yum源,非常之简单
https://www.cnblogs.com/zgqbky/p/11722032.html
1.进入yum的文件夹
命令：cd   /etc/yum.repos.d/
2.下载wget
命令：yum -y install wget
命令：yum install bash-completion          #自动补全软件包
命令：yum -y install lrzsz
3.删除yum文件夹所有yum源
命令：rm -rf    /etc/yum.repos.d/*.repo
4.利用wget下载阿里云repo文件
命令：wget  http://mirrors.aliyun.com/repo/Centos-7.repo
5.执行yum源更新命令
命令：yum clean all
命令：yum makecache
注意：依次执行
6.看一下yum仓库有多少包
命令：yum repolist


rpm
yum，自动处理rpm包依赖
yum，查看rpm包依赖关系



1. 查询软件包依赖哪些软件
rpm -qR centos-release    安装  R参数的意思就是requires就是依赖哪些软件包
rpm -qpR centos-release 未安装
或
yum deplist centos-release

2. 查询软件包被哪个软件包依赖
rpm -q centos-release # 查看这个软件是否安装 rpcbind-0.2.0-44.el7.x86_64
rpm -e --test centos-release  # 通过--test进行测试删除,查看是否有依赖关系,如果有会阻止删除
错误：依赖检测失败： rpcbind 被 (已安裝) quota-1:4.01-17.el7.x86_64 需要


yum deplist  mysql-community-common-5.7.32-1.el7.x86_64

```shell
yum deplist gcc-4.8.5-44.el7.x86_64
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Loading mirror speeds from cached hostfile
 * centos-sclo-rh: mirrors.aliyun.com
 * centos-sclo-sclo: mirrors.aliyun.com
package: gcc.x86_64 4.8.5-44.el7
  dependency: /bin/sh
   provider: bash.x86_64 4.2.46-34.el7
  dependency: /sbin/install-info
   provider: info.x86_64 5.1-5.el7
  dependency: binutils >= 2.20.51.0.2-12
   provider: binutils.x86_64 2.27-44.base.el7
  dependency: cpp = 4.8.5-44.el7
   provider: cpp.x86_64 4.8.5-44.el7
  dependency: glibc-devel >= 2.2.90-12
   provider: glibc-devel.x86_64 2.17-322.el7_9
   provider: glibc-devel.i686 2.17-322.el7_9
  dependency: ld-linux-x86-64.so.2()(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: ld-linux-x86-64.so.2(GLIBC_2.3)(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libc.so.6(GLIBC_2.14)(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libdl.so.2()(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libdl.so.2(GLIBC_2.2.5)(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libgcc >= 4.8.5-44.el7
   provider: libgcc.x86_64 4.8.5-44.el7
   provider: libgcc.i686 4.8.5-44.el7
  dependency: libgcc_s.so.1()(64bit)
   provider: libgcc.x86_64 4.8.5-44.el7
  dependency: libgmp.so.10()(64bit)
   provider: gmp.x86_64 1:6.0.0-15.el7
  dependency: libgomp = 4.8.5-44.el7
   provider: libgomp.x86_64 4.8.5-44.el7
   provider: libgomp.i686 4.8.5-44.el7
  dependency: libgomp.so.1()(64bit)
   provider: libgomp.x86_64 4.8.5-44.el7
  dependency: libm.so.6()(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libmpc.so.3()(64bit)
   provider: libmpc.x86_64 1.0.1-3.el7
  dependency: libmpfr.so.4()(64bit)
   provider: mpfr.x86_64 3.1.1-4.el7
  dependency: libz.so.1()(64bit)
   provider: zlib.x86_64 1.2.7-19.el7_9
  dependency: rtld(GNU_HASH)
   provider: glibc.x86_64 2.17-322.el7_9
   provider: glibc.i686 2.17-322.el7_9
```


rpm -qa
rpm -ql


```shell
[root@VM_0_17_centos branches]# rpm -qa | grep libodb
libodb-2.3.0-1.el7.x86_64
libodb-mysql-devel-2.3.0-1.el7.x86_64
libodb-mysql-2.3.0-1.el7.x86_64
[root@VM_0_17_centos branches]# yum deplist libodb-mysql-devel-2.3.0-1.el7.x86_64
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Loading mirror speeds from cached hostfile
 * centos-sclo-rh: mirrors.aliyun.com
 * centos-sclo-sclo: mirrors.aliyun.com
package: libodb-mysql-devel.x86_64 2.3.0-1.el7
  dependency: /usr/bin/pkg-config
   provider: pkgconfig.x86_64 1:0.27.1-4.el7
   provider: pkgconfig.i686 1:0.27.1-4.el7
  dependency: libodb-mysql(x86-64) = 2.3.0-1.el7
   provider: libodb-mysql.x86_64 2.3.0-1.el7
[root@VM_0_17_centos branches]# yum deplist libodb-mysql.x86_64 2.3.0-1.el7
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Loading mirror speeds from cached hostfile
 * centos-sclo-rh: mirrors.aliyun.com
 * centos-sclo-sclo: mirrors.aliyun.com
package: libodb-mysql.x86_64 2.3.0-1.el7
  dependency: /sbin/ldconfig
   provider: glibc.x86_64 2.17-322.el7_9
   provider: glibc.i686 2.17-322.el7_9
  dependency: libc.so.6(GLIBC_2.14)(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libgcc_s.so.1()(64bit)
   provider: libgcc.x86_64 4.8.5-44.el7
  dependency: libgcc_s.so.1(GCC_3.0)(64bit)
   provider: libgcc.x86_64 4.8.5-44.el7
  dependency: libm.so.6()(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libmysqlclient.so.18()(64bit)
   provider: mysql-community-libs-compat.x86_64 5.7.33-1.el7
   provider: mariadb-libs.x86_64 1:5.5.68-1.el7
  dependency: libmysqlclient.so.18(libmysqlclient_16)(64bit)
   provider: mysql-community-libs-compat.x86_64 5.7.33-1.el7
   provider: mariadb-libs.x86_64 1:5.5.68-1.el7
  dependency: libodb-2.3.so()(64bit)
   provider: libodb.x86_64 2.3.0-1.el7
  dependency: libpthread.so.0()(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libpthread.so.0(GLIBC_2.2.5)(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libpthread.so.0(GLIBC_2.3.2)(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libstdc++.so.6()(64bit)
   provider: libstdc++.x86_64 4.8.5-44.el7
  dependency: libstdc++.so.6(CXXABI_1.3)(64bit)
   provider: libstdc++.x86_64 4.8.5-44.el7
  dependency: libstdc++.so.6(GLIBCXX_3.4)(64bit)
   provider: libstdc++.x86_64 4.8.5-44.el7
  dependency: libstdc++.so.6(GLIBCXX_3.4.11)(64bit)
   provider: libstdc++.x86_64 4.8.5-44.el7
  dependency: libstdc++.so.6(GLIBCXX_3.4.9)(64bit)
   provider: libstdc++.x86_64 4.8.5-44.el7
  dependency: rtld(GNU_HASH)
   provider: glibc.x86_64 2.17-322.el7_9
   provider: glibc.i686 2.17-322.el7_9
```


```shell
yum repolist
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Loading mirror speeds from cached hostfile
 * centos-sclo-rh: mirrors.aliyun.com
 * centos-sclo-sclo: mirrors.aliyun.com
repo id                                                                                                  repo name                                                                                        status
!centos-sclo-rh/x86_64                                                                                   CentOS-7 - SCLo rh                                                                                7,145
!centos-sclo-sclo/x86_64                                                                                 CentOS-7 - SCLo sclo                                                                                816
!copr:copr.fedorainfracloud.org:carlwgeorge:ripgrep/x86_64                                               Copr repo for ripgrep owned by carlwgeorge                                                            3
!docker-ce-stable/x86_64                                                                                 Docker CE Stable - x86_64                                                                           100
!epel/7/x86_64                                                                                           EPEL for redhat/centos 7 - x86_64                                                                13,518
!extras/7/x86_64                                                                                         Qcloud centos extras - x86_64                                                                       448
!kubernetes/x86_64                                                                                       kubernetes                                                                                          624
!mysql-connectors-community/x86_64                                                                       MySQL Connectors Community                                                                          185
!mysql-tools-community/x86_64                                                                            MySQL Tools Community                                                                               123
!mysql57-community/x86_64                                                                                MySQL 5.7 Community Server                                                                          484
!os/7/x86_64                                                                                             Qcloud centos os - x86_64                                                                        10,072
!pgdg-common/7/x86_64                                                                                    PostgreSQL common RPMs for RHEL/CentOS 7 - x86_64                                                   387
!pgdg10/7/x86_64                                                                                         PostgreSQL 10 for RHEL/CentOS 7 - x86_64                                                            843
!pgdg11/7/x86_64                                                                                         PostgreSQL 11 for RHEL/CentOS 7 - x86_64                                                            892
!pgdg12/7/x86_64                                                                                         PostgreSQL 12 for RHEL/CentOS 7 - x86_64                                                            462
!pgdg95/7/x86_64                                                                                         PostgreSQL 9.5 for RHEL/CentOS 7 - x86_64                                                           748
!pgdg96/7/x86_64                                                                                         PostgreSQL 9.6 for RHEL/CentOS 7 - x86_64                                                           821
!updates/7/x86_64                                                                                        Qcloud centos updates - x86_64                                                                    1,630
repolist: 39,301
```


```shell
yum repolist
Loaded plugins: fastestmirror
Repository base is listed more than once in the configuration
Repository updates is listed more than once in the configuration
Repository extras is listed more than once in the configuration
Repository epel is listed more than once in the configuration
Loading mirror speeds from cached hostfile
 * webtatic: uk.repo.webtatic.com
base                                                                                                                                                                                     | 3.6 kB  00:00:00     
epel                                                                                                                                                                                     | 4.7 kB  00:00:00     
extras                                                                                                                                                                                   | 2.9 kB  00:00:00     
https://copr-be.cloud.fedoraproject.org/results/mcepl/vim8/epel-7-x86_64/repodata/repomd.xml: [Errno 14] HTTPS Error 404 - Not Found
Trying other mirror.
To address this issue please refer to the below wiki article 

https://wiki.centos.org/yum-errors

If above article doesn't help to resolve this issue please use https://bugs.centos.org/.

mysql-connectors-community                                                                                                                                                               | 2.6 kB  00:00:00     
mysql-tools-community                                                                                                                                                                    | 2.6 kB  00:00:00     
mysql56-community                                                                                                                                                                        | 2.6 kB  00:00:00     
percona-release-noarch                                                                                                                                                                   | 2.9 kB  00:00:00     
percona-release-x86_64                                                                                                                                                                   | 2.9 kB  00:00:00     
updates                                                                                                                                                                                  | 2.9 kB  00:00:00     
webtatic                                                                                                                                                                                 | 3.6 kB  00:00:00     
zabbix                                                                                                                                                                                   | 2.9 kB  00:00:00     
zabbix-non-supported                                                                                                                                                                     |  951 B  00:00:00     
(1/4): epel/x86_64/group_gz                                                                                                                                                              |  95 kB  00:00:00     
(2/4): epel/x86_64/updateinfo                                                                                                                                                            | 1.0 MB  00:00:00     
(3/4): epel/x86_64/primary_db                                                                                                                                                            | 6.9 MB  00:00:00     
(4/4): updates/7/x86_64/primary_db                                                                                                                                                       | 5.6 MB  00:00:00     
repo id                                                                                      repo name                                                                                                    status
base/7/x86_64                                                                                CentOS-7                                                                                                     10,072
epel/x86_64                                                                                  Extra Packages for Enterprise Linux 7 - x86_64                                                               13,518
extras/7/x86_64                                                                              CentOS-7                                                                                                        448
mysql-connectors-community/x86_64                                                            MySQL Connectors Community                                                                                      185
mysql-tools-community/x86_64                                                                 MySQL Tools Community                                                                                           123
mysql56-community/x86_64                                                                     MySQL 5.6 Community Server                                                                                      581
percona-release-noarch/7                                                                     Percona-Release YUM repository - noarch                                                                          63
percona-release-x86_64/7/x86_64                                                              Percona-Release YUM repository - x86_64                                                                       2,257
updates/7/x86_64                                                                             CentOS-7                                                                                                      1,630
webtatic/x86_64                                                                              Webtatic Repository EL7 - x86_64                                                                                789
zabbix/x86_64                                                                                Zabbix Official Repository - x86_64                                                                             236
zabbix-non-supported/x86_64                                                                  Zabbix Official Repository non-supported - x86_64                                                                 4
repolist: 29,906
```


`yum -y install createrepo`



# centos yum

yum源默认安装路径

rpm -qa | grep XXXXX
之后根据这个名字
rpm -ql xxx | more
就找到安装位置了.





yum - Yellowdog Updater Modified



-devel 包 包括头文件

不带devel的，只有二进制文件



yum 检索有哪些版本呢 安装指定版本



```shell
rpm -ql glog-devel
/usr/include/glog
/usr/include/glog/log_severity.h
/usr/include/glog/logging.h
/usr/include/glog/raw_logging.h
/usr/include/glog/stl_logging.h
/usr/include/glog/vlog_is_on.h
/usr/lib64/libglog.so
/usr/lib64/pkgconfig/libglog.pc
/usr/share/doc/glog-devel-0.3.3
/usr/share/doc/glog-devel-0.3.3/designstyle.css
/usr/share/doc/glog-devel-0.3.3/glog.html
```



```shell
rpm -ql gflags-devel
/usr/include/gflags
/usr/include/gflags/gflags.h
/usr/include/gflags/gflags_completions.h
/usr/include/gflags/gflags_declare.h
/usr/lib64/cmake
/usr/lib64/cmake/gflags
/usr/lib64/cmake/gflags/gflags-config-version.cmake
/usr/lib64/cmake/gflags/gflags-config.cmake
/usr/lib64/cmake/gflags/gflags-export-noconfig.cmake
/usr/lib64/cmake/gflags/gflags-export.cmake
/usr/lib64/libgflags.so
/usr/lib64/libgflags_nothreads.so
/usr/share/doc/gflags-devel-2.1.1
/usr/share/doc/gflags-devel-2.1.1/designstyle.css
/usr/share/doc/gflags-devel-2.1.1/gflags.html
```





1.使用YUM查找软件包
命令：yum search 
2.列出所有可安装的软件包
命令：yum list
3.列出所有可更新的软件包
命令：yum list updates
4.列出所有已安装的软件包
命令：yum list installed
5.列出所有已安装但不在 Yum Repository 內的软件包
命令：yum list extras
6.列出所指定的软件包
命令：yum list python
7.使用YUM获取软件包信息
命令：yum info 
8.列出所有软件包的信息
命令：yum info
9.列出所有可更新的软件包信息
命令：yum info updates
10.列出所有已安裝的软件包信息
命令：yum info installed
11.列出所有已安裝但不在 Yum Repository 內的软件包信息
命令：yum info extras
12.列出软件包提供哪些文件
命令：yum provides 
清除YUM缓存
yum 会把下载的软件包和header存储在cache中，而不会自动删除。如果我们觉得它们占用了磁盘空间，可以使用yum clean指令进行清除，更精确 的用法是yum clean headers清除header，yum clean packages清除下载的rpm包，yum clean all一 股脑儿端 

1.清除缓存目录(/var/cache/yum)下的软件包
命令：yum clean packages
2.清除缓存目录(/var/cache/yum)下的 headers
命令：yum clean headers
3.清除缓存目录(/var/cache/yum)下旧的 headers
命令：yum clean oldheaders
4.清除缓存目录(/var/cache/yum)下的软件包及旧的headers
命令：yum clean, yum clean all (= yum clean packages; yum clean oldheaders)





