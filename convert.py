from docx import Document
from docx.oxml import parse_xml
import mathml2omml
from sympy.printing.mathml import print_mathml
from sympy import *


document = Document()

p = document.add_paragraph()
omml_xml = '<p xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:oMathPara><m:oMath><m:f><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:r><m:t>2</m:t></m:r></m:den></m:f></m:oMath></m:oMathPara></p>'
omml_el = parse_xml(omml_xml)[0]
p._p.append(omml_el)


mathml = "<math><mi>x</mi><mo>+</mo><mi>y</mi></math>"
omml = mathml2omml.convert(mathml)

results = (
  f'<p xmlns:m="http://schemas.openxmlformats.org/officeDocument'
  f'/2006/math">{omml}</p>'
)
omml_el2 = parse_xml(results)[0]
p._p.append(omml_el2)
#
# x, y, z, t = symbols("x y z t")
#
# obj = print_mathml(Integral(sqrt(1 / x), x))
obj = '<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mi>x</mi><mo>=</mo><mfrac><mrow><mo>-</mo><mi>b</mi><mo>±</mo><msqrt><mrow><msup><mi>b</mi><mn>2</mn></msup><mo>-</mo><mn>4</mn><mi>a</mi><mi>c</mi></mrow></msqrt></mrow><mrow><mn>2</mn><mi>a</mi></mrow></mfrac></math>'
omml3 = mathml2omml.convert(obj)
results2 = (
  f'<p xmlns:m="http://schemas.openxmlformats.org/officeDocument'
  f'/2006/math">{omml3}</p>'
)
omml_el3 = parse_xml(results2)[0]
p._p.append(omml_el3)

from sympy import *

i, j = symbols("i j", cls=Idx)
sum2 = Sum(Sum(Indexed("a", i) * Indexed("b", j), (i, 0, 2)), (j, 0, 2))
latex_strings = latex(sum2)

import latex2mathml.converter

mathml_output = latex2mathml.converter.convert(latex_strings)

omml3 = mathml2omml.convert(mathml_output)
results2 = (
  f'<p xmlns:m="http://schemas.openxmlformats.org/officeDocument'
  f'/2006/math">{omml3}</p>'
)
omml_el3 = parse_xml(results2)[0]
p._p.append(omml_el3)

document.save("demo5.docx")
