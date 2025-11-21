# odata

OData is a protocol to expose (as you stated) Data As a REST Resource. The page to go to learn more is [http://www.odata.org](http://www.odata.org/).

WCF Data Services is an implementation of the OData protocol (both client and server) by Microsoft on the .NET platform. So a service created by WCF Data Services uses the OData protocol.

ATOM is a standard format, and it is one of the possible wire formats for transferring data in the OData protocol. The OData protocol defines extensions to it. For better picture, ATOM is an XML based format which defines XML elements and their meaning (feeds, entries, links), and OData uses that along with couple of its own XML elements to serialize the data.

JSON is a standard format (for serialization of JavaScript objects) and it is one of the possible wire formats for transferring data in the OData protocol. So OData protocol uses JSON to serialize the data.