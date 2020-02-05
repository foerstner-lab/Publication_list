Find our articles with us in `author_name_string` and not as
`author_name` property:

```
SELECT ?item
WHERE
{

  {?item wdt:P2093 "Konrad U Foerstner"}
  UNION
  {?item wdt:P2093 "Konrad Foerstner"}
  UNION
  {?item wdt:P2093 "Konrad Förstner"}
  UNION
  {?item wdt:P2093 "Konrad U. Förstner"}
  UNION
  {?item wdt:P2093 "Konrad U Förstner"}
  UNION
  {?item wdt:P2093 "Konrad U. Foerstner"}
  UNION
  {?item wdt:P2093 "Konrad Ulrich Förstner"}

}
```
