# xsd

[XSD文件详解](https://www.cnblogs.com/sjqq/p/8318278.html)

Spring xsd文件自定义标签



beans

tx







以Dubbo的xsd文件为例

xsd:element

- annotation

- application

- module

- registry

- monitor

- provider

- consumer

- protocol

- service

- reference

- method

- argument

- parameter

<xsd:element name="annotation" type="annotationType">

annotationType在<xsd:complexType name="annotationType">中定义
