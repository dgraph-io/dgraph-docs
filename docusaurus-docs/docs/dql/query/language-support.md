---
title: Language Support
---
import RunnableCodeBlock from '@site/src/components/RunnableCodeBlock';




:::noteA `@lang` directive must be specified in the schema to query or mutate
predicates with language tags.:::

Dgraph supports UTF-8 strings.

In a query, for a string valued edge `edge`, the syntax
```
edge@lang1:...:langN
```
specifies the preference order for returned languages, with the following rules.

* At most one result will be returned (except in the case where the language list is set to *).
* The preference list is considered left to right: if a value in given language is not found, the next language from the list is considered.
* If there are no values in any of the specified languages, no value is returned.
* A final `.` means that a value without a specified language is returned or if there is no value without language, a value in ''some'' language is returned.
* Setting the language list value to * will return all the values for that predicate along with their language. Values without a language tag are also returned.

For example:

- `name`   => Look for an untagged string; return nothing if no untagged value exits.
- `name@.` => Look for an untagged string, then any language.
- `name@en` => Look for `en` tagged string; return nothing if no `en` tagged string exists.
- `name@en:.` => Look for `en`, then untagged, then any language.
- `name@en:pl` => Look for `en`, then `pl`, otherwise nothing.
- `name@en:pl:.` => Look for `en`, then `pl`, then untagged, then any language.
- `name@*` => Look for all the values of this predicate and return them along with their language. For example, if there are two values with languages en and hi, this query will return two keys named "name@en" and "name@hi".


:::note

In functions, language lists (including the `@*` notation) are not allowed.
Untagged predicates, Single language tags, and `.` notation work as described
above.

---
In [full-text search functions](/dgraph-overview/functions#full-text-search)
(`alloftext`, `anyoftext`), when no language is specified (untagged or `@.`),
the default (English) full-text tokenizer is used. This does not mean that
the value with the `en` tag will be searched when querying the untagged value,
but that untagged values will be treated as English text. If you don't want that
to be the case, use the appropriate tag for the desired language, both for
mutating and querying the value.
:::
Query Example: Some of Bollywood director and actor Farhan Akhtar's movies have a name stored in Russian as well as Hindi and English, others do not.
<RunnableCodeBlock>

```dql
{
  q(func: allofterms(name@en, "Farhan Akhtar")) {
    name@hi
    name@en
    director.film {
      name@ru:hi:en
      name@en
      name@hi
      name@ru
    }
  }
}
```

</RunnableCodeBlock>