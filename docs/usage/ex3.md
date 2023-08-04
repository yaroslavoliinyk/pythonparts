# Heading 1

Hallo world!

```{note}
An admonition note!
```

[Link to the heading](#heading-1)

## Math

```python
from package import module
module.call("string")
```

## Definition list

term
: definition

## Math

$$\pi = 3.14159$$

## Figures

```{figure} https://via.placeholder.com/150
:width: 100px
:align: center

Figure caption
```

## Tables

```{list-table}
:header-rows: 1
:align: center

* - Header 1
  - Header 2
* - Item 1 a
  - Item 2 a
* - Item 1 b
  - Item 2 b
```

### Heading Level 3

> {.bg-primary}
> ### Paragraph heading

* * *

{.bg-primary}
Here is a paragraph with a class to control its formatting.

A paragraph with a span of [text with attributes]{.bg-warning}

> We know what we are, but know not what we may be.

{attribution="Hamlet act 4, Scene 5"}
> We know what we are, but know not what we may be.


Term 1
: Definition

Term 2
: Longer definition

  With multiple paragraphs

  - And bullet points


:::{tip}
:class: myclass1,myclass2
:name: a-tip-reference
Let's give readers a helpful hint!
:::

[Reference to my tip](#a-tip-reference)


:::{versionadded} 1.2.3
Explanation of the new feature.
:::

:::{versionchanged} 1.2.3
Explanation of the change.
:::

:::{deprecated} 1.2.3
Explanation of the deprecation.
:::


:::{note}
:class: dropdown

This admonition has been collapsed,
meaning you can add longer form content here,
without it taking up too much space on the page.
:::