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


   
   **Route out of this page**
 
Tapping a society card pushes ``UserSocietyPage``, passing three named arguments:
 
.. code-block:: dart
 
   Navigator.push(
     context,
     MaterialPageRoute(
       builder: (_) => UserSocietyPage(
         societyId: id,
         societyName: name,
         description: description,
       ),
     ),
   );
 

.. list-table::
   :widths: 25 15 60
   :header-rows: 1
 
   * - Argument
     - Type
     - Description
   * - ``societyId``
     - ``int``
     - The unique ID of the selected society.
   * - ``societyName``
     - ``String``
     - Display name passed directly to avoid a second network call.
   * - ``description``
     - ``String``
     - Society description passed directly to avoid a second network call.