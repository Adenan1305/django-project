from pathlib import Path

# Reuse the report's page setup and document helpers, without its content.
source = Path(__file__).with_name('build_report.py').read_text(encoding='utf-8')
exec(source[:source.index("p('รายงานโครงงาน")])
for name in ['Normal', 'Title', 'Heading 1', 'Heading 2']:
    doc.styles[name].font.name = 'Calibri'
    doc.styles[name].element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:cs'), 'Calibri')
doc.styles['Normal'].paragraph_format.line_spacing = 1.15

def body(*texts):
    for text in texts: p(text)

p('Web Programming Project Report', 'Title').alignment = WD_ALIGN_PARAGRAPH.CENTER
p('Development of a Restaurant Website\nwith Natural Language Food Ordering\nUsing the OpenRouter API', 'Title').alignment = WD_ALIGN_PARAGRAPH.CENTER
p('Noodle Shop').alignment = WD_ALIGN_PARAGRAPH.CENTER
for _ in range(3): p('')
for text in ['Prepared by', 'Full Name ........................................................', 'Student ID ........................................................', 'Program and Year ..............................................', '', 'Submitted to', 'Instructor ........................................................', '', 'Submitted as part of the Web Programming course', 'Semester ............ Academic Year ............', 'Institution ........................................................']:
    p(text).alignment = WD_ALIGN_PARAGRAPH.CENTER

page('Abstract and Objectives')
h('Abstract')
body('This project develops Noodle Shop, a restaurant website that allows customers to browse a menu, manage a shopping cart, and submit orders through a web browser. An AI assistant provides an additional ordering method: customers enter a natural language request, such as “Two chicken noodles with thin noodles and extra egg.” The server sends the request to the OpenRouter API, validates the returned data, and supplies items for the browser to add to the cart. Customers review the cart before submitting their orders.',
'The website uses HTML, CSS, and JavaScript for its user interface, Python and Django for server processing, and SQLite for order and member points data. The design separates AI interpretation from business rules: the AI identifies requested items, while the restaurant application validates product identifiers, determines prices, and records purchases.',
'Additional features include registration, sign-in, member points, reward redemption, receipts, and administration through Django Admin. In the current implementation, natural language input is typed text. Microphone input and speech recognition are proposed extensions.')
h('Background')
p('Ordering several dishes with different options can require repeated menu interactions. A natural language interface offers another way to express the same request. This project explores how a web application can integrate an external AI service while retaining control over its catalog and order records.')
h('Objectives')
body('1. Develop a restaurant website for menu browsing and order submission.', '2. Integrate OpenRouter to interpret natural language food requests.', '3. Validate AI output against the restaurant catalog.', '4. Combine Django, database models, JavaScript, HTTP, and JSON.', '5. Allow customers to review items before confirming an order.')

page('Chapter 1 Scope and Technologies')
h('System Scope')
body('Guests can browse the menu, use the AI ordering field, manage a cart, and submit orders. Registered members can also earn points and redeem eligible rewards. Administrators manage order records through the administration interface. Defined order statuses are pending, preparing, completed, and cancelled.',
'The server catalog contains 12 products across combo meals, rice, noodles, drinks, dessert, and snacks. The AI interface accepts noodle values of Thin, Wide, egg noodles, or an empty string when not applicable. Extra egg is represented as a Boolean option.')
table(['Technology', 'Role in the Project'], [
('HTML and Django Templates', 'Structure the home, menu, cart, receipt, and account pages.'),
('CSS', 'Style customer pages and the administration interface.'),
('JavaScript', 'Handle interactions, local cart data, and API requests through fetch.'),
('Python and Django', 'Process requests, validate data, authenticate users, and save orders.'),
('SQLite and Django ORM', 'Store application data and manage model relationships.'),
('OpenRouter API', 'Provide access to a language model for interpreting food requests.'),
('OpenAI Python SDK', 'Call OpenRouter using a configured base_url.')])
h('Core Concepts')
body('Django separates data models, request handling views, and page templates. The AI feature uses HTTP requests with JSON bodies, allowing JavaScript to submit a message and display results without navigating to another page.',
'OpenRouter provides an API format similar to the OpenAI Chat API, enabling the client integration used in this project [1]. Django models define stored data and database relationships [2].')

page('Chapter 2 Architecture and Database Design')
h('System Architecture')
body('Browser → Django server → OpenRouter → Language model\nLanguage model → OpenRouter → Django validation → Browser cart\nCustomer order confirmation → Django → SQLite → Receipt page',
'The browser calls the website’s own endpoints. Django contacts OpenRouter using a server-side API key, which is not included in the frontend JavaScript. An AI response adds items to the cart; it does not directly create a database order. The order is saved only when the customer submits checkout data.')
h('Main Data Models')
table(['Model', 'Stored Data and Relationships'], [
('User', 'Member accounts provided by Django’s standard authentication system.'),
('Order', 'Customer, payment method, status, subtotal, tax, total, and creation time. The customer may be null for guest orders.'),
('OrderItem', 'Order reference, product ID, name, price, quantity, noodle option, egg option, and reward flag.'),
('UserPoints', 'A one-to-one relationship with User that stores the member’s points balance.')])
body('A user can have multiple orders, and each order can contain multiple order items. Each member has one points record. Deleting an order also deletes its associated items. If a user account is deleted, the linked order can remain with a null customer reference.')
h('Catalog and Cart Storage')
body('The server maintains product names and base prices in PRODUCT_CATALOG. Products are not represented by a separate Product database table. The browser stores its cart in localStorage. A combined key based on product ID, noodle option, and egg option distinguishes item configurations; identical configurations have their quantities combined.',
'At checkout, the server retrieves prices from its own catalog rather than trusting prices supplied by the browser. OrderItem stores the price associated with that purchase.')

page('Chapter 3 Website Functionality')
table(['Feature', 'Behavior'], [
('Home and Menu', 'Display restaurant information, available dishes, and the AI ordering field.'),
('Shopping Cart', 'Display items, quantities, options, and the order summary.'),
('Member Accounts', 'Support registration, sign-in, and sign-out.'),
('Order Submission', 'Validate checkout data and create Order and OrderItem records.'),
('Receipts', 'Display order details to customers who are authorized to access them.'),
('Points and Rewards', 'Allow members to earn points and redeem configured products.'),
('Administration', 'Provide Django Admin pages with customized styling.')])
h('Ordering Workflow')
p('Customers select dishes from the menu or enter a request in the AI field. They review the cart and select a payment method. The browser submits checkout data to /orders/create/. The server validates product identifiers, quantities, and the payment method. After successful storage, it returns a URL for the receipt page.')
h('Pricing and Member Points')
body('The implementation adds 10 baht per unit when extra egg is selected. It computes its tax field as subtotal multiplied by 0.07 and uses Decimal with rounding to two decimal places. Members earn one point for every complete 10 baht of the subtotal. Guests do not earn member points.',
'Configured rewards are ice cream and fried meatballs, each costing 300 points. Redemption requires authentication, a sufficient points balance, and valid reward item options. Order creation and points updates are performed within transaction.atomic to keep related database changes together.')
h('Payment Method Selection')
p('The configured payment methods are PromptPay and Cash. The order record stores the selected method. Selecting PromptPay does not establish that a bank transfer has been automatically verified. Integrating payment confirmation is a possible extension.')

page('Chapter 4 AI Ordering and OpenRouter Integration')
h('Receiving Customer Input')
body('The submitAIOrder function in ai-order.js reads the input field and sends a POST request to /api/ai-order/. It includes an application/json content type and an X-CSRFToken header. An example request body is {"message": "Two chicken noodles with thin noodles and extra egg"}. While awaiting a response, the interface disables the order button and displays a processing message.',
'The ai_order view requires POST and a JSON object. The message must be a nonempty string of at most 1,000 characters. The view also checks that OPENROUTER_API_KEY is configured before contacting the external service.')
h('Prompt and API Configuration')
body('The server builds a system prompt containing product IDs, names, prices, categories, and designated popular products. It instructs the model to return JSON with items, clarification, and assistant_message. The model is directed to use only catalog products, avoid inventing IDs or prices, and reply in the customer’s language.',
'The OpenAI Python SDK is configured with base_url set to https://openrouter.ai/api/v1. The application calls client.chat.completions.create with the model identifier apodex/apodex-1.1-mini:free and response_format set to json_object. This identifier is the value configured in the project; live use depends on the provider’s current model availability.')
h('Response Types')
p('For a clear purchase request, the model returns items. For an unclear request, it returns a clarification question. For a recommendation request, it returns assistant_message without cart items. Each API call sends the current customer message and system prompt; the current implementation does not send an ongoing conversation history.')
h('Server Validation')
p('Django checks that each product exists, that quantity is an integer from 1 to 99, that the noodle value is permitted, and that egg is Boolean. It then adds the product name and base price from the server catalog. Invalid results are rejected. JSON output mode supports parsing, while server validation enforces the application’s data requirements.')

page('Chapter 5 Usage Example and Testing')
h('Expected Ordering Example')
body('For “Two chicken noodles with thin noodles and extra egg,” the expected item has product_id 5, quantity 2, noodle "Thin", and egg true. Django adds the name Chicken noodles and the base price "50.00". JavaScript adds the validated item to the cart. The extra egg charge and final order totals are calculated during checkout.',
'This example describes the intended data format and behavior. It is not a measured result from a live model evaluation.')
table(['Test Scenario', 'Expected Behavior'], [
('Named dish with quantity and extra egg', 'Return validated item data with the catalog price.'),
('Two servings of dessert', 'Return dessert items totaling two servings.'),
('Three different snacks', 'Return three distinct products from the snack category.'),
('Ambiguous request', 'Return a clarification question.'),
('Menu recommendation request', 'Return assistant_message without adding cart items.'),
('Invalid model item', 'Reject invalid identifiers or data before returning items.'),
('GET request or malformed JSON', 'Return HTTP 405 or HTTP 400, respectively.'),
('Missing API key', 'Return HTTP 503 without calling the AI service.')])
h('Existing Test Approach')
body('home/tests.py contains AIOrderTests and tests for authentication, orders, points, rewards, and receipt access. AI tests mock the OpenRouter client to control its response and check application behavior reproducibly. These tests verify integration logic; their presence does not establish the accuracy of the live language model.',
'A live evaluation should use varied customer requests, including Thai wording, and record correctness of dishes, quantities, and options. Response time, error counts, and sample size should also be recorded before making quantitative performance claims.')

page('Chapter 6 Limitations and Future Development')
h('Current Limitations')
body('AI ordering depends on internet access, OpenRouter availability, and the configured model. A response can have valid structure while still misunderstanding the customer’s intent. Customers therefore need to review their cart before confirming the order.',
'The current interface accepts typed text and does not implement microphone input or speech-to-text conversion. It does not maintain a continuous AI conversation. Catalog information exists in both server code and frontend JavaScript, so menu changes require keeping these definitions consistent. A localStorage cart can be lost when browser data is cleared.')
h('Validation and Error Handling')
p('The application uses CSRF tokens for frontend requests, stores the API key on the server, and validates AI items before use. Order and receipt handling distinguish account users from guests. Service errors or unreadable JSON produce error responses rather than new cart items. Prompt instructions discourage following unrelated instructions inside a customer message, but server validation remains necessary.')
h('Proposed Improvements')
body('1. Add speech recognition and send the transcribed text to the existing API.',
'2. Move products into a database table editable through administration pages.',
'3. Maintain conversation context for follow-up answers and order changes.',
'4. Add request rate limits, explicit timeouts, and API cost monitoring.',
'5. Integrate payment verification and customer order status tracking.',
'6. Evaluate the AI with varied Thai requests and real users before broader deployment.')
h('Expected Benefits')
p('The project demonstrates practical integration of web programming and an external AI service. It provides experience in data modeling, API communication, validation of external outputs, and order management. Customers gain an additional way to express their food requests alongside conventional menu selection.')

page('Conclusion and References')
h('Conclusion')
body('Noodle Shop combines menu browsing, cart management, member accounts, orders, points, receipts, and administration in a Django application. The OpenRouter API helps convert natural language food requests into structured item data. The restaurant application remains responsible for catalog validation, pricing, and order storage.',
'The project shows that useful AI integration requires both data validation and customer review. Future work can extend the application with voice input, a database-backed catalog, conversational context, payment verification, and systematic evaluation under real usage conditions.')
h('References')
body('[1] OpenRouter. API Reference. Accessed October 11, 2026.\nhttps://openrouter.ai/docs/api_reference/overview',
'[2] Django Software Foundation. Models. Django 6.0 Documentation. Accessed October 11, 2026.\nhttps://docs.djangoproject.com/en/6.0/topics/db/models/',
'[3] Noodle Shop project source code. Files examined include home/views.py, home/models.py, home/urls.py, home/tests.py, config/settings.py, and home/static/home/js/ai-order.js.')
h('Appendix Key Project Files')
table(['File', 'Purpose'], [
('home/views.py', 'Handle AI requests, authentication, orders, and points.'),
('home/models.py', 'Define Order, OrderItem, and UserPoints.'),
('home/urls.py', 'Map website and API routes.'),
('home/templates/home/', 'Provide customer-facing page templates.'),
('home/static/home/js/', 'Implement frontend interactions and cart logic.'),
('home/tests.py', 'Define application test cases.'),
('requirements.txt', 'Declare Django and openai dependencies.')])

footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
field = OxmlElement('w:fldSimple'); field.set(qn('w:instr'), 'PAGE'); footer._p.append(field)
doc.core_properties.title = 'Restaurant Website with Natural Language Food Ordering'
doc.core_properties.subject = 'Web Programming and OpenRouter API'
doc.core_properties.author = ''
target = OUT / 'Noodle_Shop_Web_Programming_Report_English.docx'
doc.save(target)
from zipfile import ZipFile
import re
with ZipFile(target) as archive:
    assert archive.testzip() is None
    for name in archive.namelist():
        if name.endswith('.xml'):
            assert not re.search('[\u0e00-\u0e7f]', archive.read(name).decode('utf-8')), name
print(target)
print('Verified: no Thai characters in document XML.')
