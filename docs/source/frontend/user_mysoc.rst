User MySoc Page
======================
 
Overview
--------
 
The **MySoc** page displays all societies the authenticated user is currently an active
member of. It is one of the main navigation destinations for regular (non-admin) users and acts
as the entry point to individual society pages.
 
The page is implemented as the ``MySocietyPage`` stateful widget, found at
``lib/screens/user_mysoc_page.dart``.
 
---



Navigation
----------
 
**Route into this page**
 
``MySoc`` is typically reached from the main bottom navigation bar or home screen.
No arguments are required to construct it.
 
.. code-block:: dart
 
   Navigator.push(
     context,
     MaterialPageRoute(builder: (_) => const MySocietyPage()),
   );