+++
title = "Deprecation"
weight = 8
[menu.main]
    parent = "schema"
+++

The `@deprecated` directive allows you to tag the schema definition of a field or enum value as deprecated with an optional reason.

When you use the `@deprecated` directive, GraphQL users can deprecate their use of the deprecated field or `enum` value.
Most GraphQL tools and clients will pick up this notification and give you a warning if you try to use a deprecated field.

### Example

For example, to mark `oldField` in the schema as deprecated:

```graphql
type MyType {
  id: ID!
  oldField: String @deprecated(reason: "oldField is deprecated. Use newField instead.")
  newField: String
  deprecatedField: String @deprecated
}
```
