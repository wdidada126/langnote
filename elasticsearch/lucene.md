# lucene

https://lucene.apache.org/

D:\git\github\elasticsearch\buildSrc\version.properties

elasticsearch     = 7.9.3
lucene            = 8.6.2

## maven pom

## gradle pom
  api "org.apache.lucene:lucene-core:${versions.lucene}"
  api "org.apache.lucene:lucene-analyzers-common:${versions.lucene}"
  api "org.apache.lucene:lucene-backward-codecs:${versions.lucene}"
  api "org.apache.lucene:lucene-grouping:${versions.lucene}"
  api "org.apache.lucene:lucene-highlighter:${versions.lucene}"
  api "org.apache.lucene:lucene-join:${versions.lucene}"
  api "org.apache.lucene:lucene-memory:${versions.lucene}"
  api "org.apache.lucene:lucene-misc:${versions.lucene}"
  api "org.apache.lucene:lucene-queries:${versions.lucene}"
  api "org.apache.lucene:lucene-queryparser:${versions.lucene}"
  api "org.apache.lucene:lucene-sandbox:${versions.lucene}"
  api "org.apache.lucene:lucene-spatial-extras:${versions.lucene}"
  api "org.apache.lucene:lucene-spatial3d:${versions.lucene}"
  api "org.apache.lucene:lucene-suggest:${versions.lucene}"