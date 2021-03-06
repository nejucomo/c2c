============================
c2c - Connect to Certificate
============================

Overview
========

`c2c` is an alternative certificate verification and network resolution strategy, which:

* can be used with existing TLS software,
* provides `reference author` authentication properties in contrast to standard TLS-based PKI's `Certificate Authority Common-Name-based` authentication,
* does not rely on Certificate Authorities (CAs),
* does not rely on Domain Naming System (DNS),
* can be used by cooperating TLS clients without knowledge or coordination from existing TLS servers,
* allows `certificate owner-based authority` over IP resolution,
* consists of complementary, yet decoupled, conventions for selective or partial adoption and deployment,
* and is designed with web browser security in mind.

Summary
-------

`c2c` clients refer to TLS servers by their certificate's hash using an exceptional pseudo-TLD ``.c2c``.  These pseudo-domains are called `c2c addresses`.  An example c2c address: ``ahqaceowa9oqbjgz56urj1573ro.a.c2c``

When given such a reference to initiate a connection, TLS verification of the server certificate, they require the server-presented certificate to hash to the given pseudo-domain.

Because the pseudo-domain is not a valid `DNS` name, alternative resolution approaches are possible, the simplest being `immediate resolution` where the pseudo-domains encode IP addresses as well as certificate fingerprints, such as: ``224.154.80.208.ip4.ahqaceowa9oqbjgz56urj1573ro.a.c2c``

Use Cases
---------

`c2c` is a suitable choice for network design and architecture in cases where self-validating server references are superior to third party CA attestations.  This distinction implies some fundamental differences in network architecture:

* In a `c2c` based network, domain names are not used for human-readability (although DNS may still be used for IP resolution).
* `c2c` is agnostic about client-side certificate verification.
* `c2c addresses` are inexorably bound to a specific certificate, so that certificate rotation, revocation, and other key management issues require understanding and potentially modifying clients.
* Because `c2c` clients do not rely on CAs, the policy and management issues of third-party authorities is absent.

Complementary and Overlapping Use
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It may be possible to use some `c2c` features as complementary or overlapping to traditional TLS PKI and DNS.

For example, the same TLS server may be reachable via `DNS` and serve a CA-signed certificate bound to the domain by ``CN``.  *Additionally*, some subset of clients may also reach and verify the same server using a distinct `c2c address`.  The mixture of two strategies is partitioned among clients in this example.

A different mixture of strategies is within a single client's verification logic, where both CA *and* `c2c` verification is performed.  (Note: this example is deliberately hand-wavy because in the short term this kind of use case is out of scope.)

Example Use Case
~~~~~~~~~~~~~~~~

Suppose a large network service uses a VPS system to rapidly deploy debian-based virtual machines.  The service has an internal package repository for these VPS guests.  The guests may be initially launched with a `c2c address` in the `apt` ``sources.list`` file.  After a guest is launched, package updates can use the standard `apt-get` upgrade mechanism.

Because the service uses `c2c addresses`, there is no need to manage `DNS` entries or CA signatures on the internal package repository host, saving cost and complexity.  Because the ``sources.list`` file is managed by devops engineers and rarely altered, there is little need for human-meaningful names (similar to an ``~/.ssh/authorized_keys`` file, for example).

Redeployment of the guests is low cost, so in the event that the package repository certificate must be rotated, a new guest deployment cycle can upgrade the `c2c addresses` used by ``apt``.  This is an example of a custom, feasible key rotation mechanism, even though `c2c` itself is agnostic about key management.

Security
........

Assume that the VPS deployment process and the source of the ``sources.list`` file are not compromised by an attacker, and also that `apt` package signing is disabled (which is hopefully rare in modern times).  In the traditional case of securing communication with the package repository by ``https`` URLs, a compromised CA can enable an active interception attack (aka "man in the middle") to inject malicious packages.  By contrast, after the `c2c`-based VPS deployment is complete, an attacker cannot execute such an interception attack, and must instead compromise something aside from TLS authentication (eg: the repository or installing VPS hosts, or other areas of the TLS protocol)

Related Architectures
~~~~~~~~~~~~~~~~~~~~~

The `Tor` network provides a hidden service feature with similar properties to `c2c`.  Hidden service addresses encode sufficient information to cryptographically verify a connection based on the address contents.  The hidden service protocol does not rely on TLS for end-to-end security (**FIXME:** Verify this is true), and does not rely on CAs for verifying remote endpoint legitimacy.

A feature goal for hidden services is to protect clients from discovering a server's IP address (as the name implies), which is not a `c2c` feature.


Real Life Usage
~~~~~~~~~~~~~~~

Currently `c2c` is merely a gleam in the eye of some hacker and some prototype code, so it would not be conservative to design a new datacenter operations automation system built on a `c2c` strategy from the ground up.

Additionally, it requires client-modifications or proxies to be useful, so use cases targetting mass client adoption are ill-suited.

Specification
=============

.. caution:: Everything here is provisional and there are unresolved major decisions such as what verification actually means (ie: hash of complete chain?  Leaf-node pubkey hash?).  This "specification" currently exists just to give some details to chew on.

`c2c` is composed of three layers of specification:

#. `c2c verification` - the algorithm and it's requisite parameters for verifying a certificate.
#. `c2c addresses` - the format, constraints, and intended use of addresses.
#. `c2c resolution` - the protocol by which `c2c addresses` are resolved to IP addresses.

The layers build on prior layers, and prior layers may be used without further extensions.  For example, it is possible to use `c2c verification` in a system which does not use `c2c addresses` provided that alternative system supplies the necessary parameters for verification.

Specification Revision
----------------------

This specification is informal, unreviewed, and potentially ambiguous, and presently known only as `c2c Specification rev0'.  Because of the prototypical nature of this repository and specification, we expect multiple different potentially incompatible versions of a `c2c specification` which all claim to be `rev0`, so interoperability and security analysis cannot rely on this versioning without careful examination of specific code or deployments.

c2c Verification
----------------

`c2c verification` encompasses a potential family of verification techniques, each with a well known distinct specification name.  The only technique defined as of this writing is `c2c verification direct`:

c2c Verification Direct
~~~~~~~~~~~~~~~~~~~~~~~

Required parameters
...................

* A `TLS candidate certificate`, such as that presented by a server during a handshake.  (Note: There is no distinction between the certificate's semantic content and a specific bitstring encoding the certificate.)
* A `hash algorithm specifier`.  Currently only ``FIXME`` is defined.
* An `asserted certificate hash`.  Note: This is a distinct and independent parameter from the `TLS candidate certificate`.  (If it were computed from the candidate certificate, the system would provide no noticeable desired behavior at a notable complexity and overhead cost.)  Also, it is an unencoded raw bitstring.

Process
.......

The hash of the `TLS candidate certificate` bitstring is computed according to the `hash algorithm specifier` to produce a `candidate hash`.  If the `candidate hash` is bitwise identical to the `asserted certificate hash`, then verification succeeds.  Otherwise verification fails.

**Implementation Note:** A cautious implementation should strive to avoid timing attacks, such as by doing a constant-time comparison of the `candidate` and `asserted` hashes.  (**FIXME:** we need a security model; the assumption here is that remote entities should not know which `c2c address` the client uses from this verification process as a privacy protection.)

c2c Addresses
-------------

A `c2c address` must match the constrains placed on domain names as per `DNS`.  (**FIXME:** Refer to a specific reference standard.)  The following conditional constraints and semantics apply:

The domain parts (**FIXME:** use `DNS` terminology) are called `address fields`.  The constraints and semantics of a field depend on its content, as well as address fields to its right (ie: parent pseudo-domains), but *exclude* fields to the left (ie: child pseudo-domains).  Additionally, for a given parent pseudo-domain the `field index` (defined by the number of ``.`` characters to the right of a given field) determines the semantic intepretation unambiguously.

There are three ``field groups`` presented in the same order, one being optional, so that every domain follows this high level syntax::

    [ «resolution group» '.' ] «verification group» '.' «pseudo top level domain»

Examples
~~~~~~~~

An example without a `resolution group` is::

    ahqaceowa9oqbjgz56urj1573ro.a.c2c

An example with a `resolution group` is::

    224.154.80.208.ip4.ahqaceowa9oqbjgz56urj1573ro.a.c2c

In the latter example, the `resolution group` is the five fields ``224.154.80.208.ip4``, the `verification group` is the two fields ``ahqaceowa9oqbjgz56urj1573ro.a``, and the `pseudo-TLD` is ``c2c``.

Pseudo Top Level Domain
~~~~~~~~~~~~~~~~~~~~~~~

The `Pseudo Top Level Domain` (aka `Pseudo-TLD`) is always ``c2c``.  (**Note:** This is provisional until we research `gtld` registrations to determine a `Pseudo-TLD` which cannot collide with legitimate `DNS` addresses.)  This specified constant serves two purposes:

#. It is not a valid `DNS` top-level domain, and also cannot be registered as one in the future, and
#. It therefore can distinguish domain names between `c2c addresses` and standard `DNS` domains (or other non-standard domains, such as the Tor Pseudo-TLD ``.onion``).

Verification Group
~~~~~~~~~~~~~~~~~~

The verification group is the lynchpin of the `c2c address` scheme and critical to its security properties.  The top-most field in this group (thus always the second-level address field) specifies the `c2c Verification` method and the other fields in this group provide sufficient assertion parameters for the given verification method.

Verification Method Field
.........................

In this spec revision, the only verification method is `c2c verification direct` which is represented by the constant ``a``.  Thus, as of this revision, every ``c2c address`` must end with `.a.c2c`.

For direct verification, the field group always has this form:

    «hash assertion field» ".a"

The `hash assertion field` consists of a `hash method indicator` prefix followed by an encoded `hash assertion`.  As of this revision the only `hash method indicator` is the constant ``'a'`` and the semantics are defined as follows:

**Hash Method 'a' - Encoding:** Compute the ``SHA256`` of the server's TLS certificate bitstring as it will be presented during a `TLS` handshake, then truncate the result to the leftmost 16 bytes, and encode this using `zbase32`.  (**FIXME:** fully specify `zbase32`.  For now the specification is "just like the python `zbase32` library has done it in the past most stable release.)

An example verification group is::

    ahqaceowa9oqbjgz56urj1573ro.a

Note that the initial ``a`` provides versioning on the hashing scheme, and the final ``a`` provides versioning on the verification method.

Resolution Group
~~~~~~~~~~~~~~~~

The resolution group is optional and supplies information for clients to resolve a `c2c address` to an IP address.  As in the verification group, the topmost field in this group is a `resolution method field` and the remaining fields are interpreted according to this method as parameters to some resolution system.

Absent Resolution
.................

Without a resolution group present, clients are left to their own devices to discover the IP address for the given certificate.  This may be acceptable, for example, in a tightly knit network application where resolution is already well specified by context and the benefit to shorter addresses is preferable.  In a more general context, widely deployed clients may use a common default resolution system, which if ubiquitous would allow shorter addresses to widely propagate.

Direct IP Resolution
....................

The direct IP resolution mechanism is specified by a `resolution method field` of ``a`` and encodes an IP address into the `c2c address`.  Clients resolve the `c2c address` to an IP address merely by decoding this field.  There is no networking or client-state involved in direct resolution.

There is always exactly one sub-field for this resolution method which consists of a prefix to specify the IP encoding followed by the encoded IP address:

**Compact Direct IP Encoding:** The prefix ``a`` is followed by the `zbase32` encoding of the raw IP bits.  Both `IPv4` and `IPv6` addresses may be encoded and are distinguished by their length.  (**Note:** This encoding may be larger than a transparent IPv6 encoding which uses some of the standard IPv6 ASCII encoding compressions.)

**Transparent IPv4 Encoding:** The prefix ``ipv4-`` is followed by the dotted-quad representation of the IPv4 address except each ``.`` is replaced with ``-``.  (**FIXME:** Does reverse DNS already specify the kind of encoding we want here?)

**Transparent IPv6 Encoding:** **FIXME:** Todo.

DNS Resolution
..............

`c2c` can combine its alternative verification method with `DNS` resolution to support existing infrastructure and reduce "address brittleness".  In this case the `resolution method field` is ``dns``.

Unlike all formerly specified field groups, this field group is unique in that the number of sub-fields is not fixed.  All subfields beyond the ``dns`` `resolution method field` compose a legitimate DNS entry.  To resolve such addresses, clients construct a new domain from these subfields and then use standard DNS for IP resolution.

Example::

    example.com.dns.ahqaceowa9oqbjgz56urj1573ro.a.c2c

Clients would resolve this ``dns`` resolution method `c2c` address by constructing a domain from all fields left of ``dns`` to derive ``example.com``, and then use `DNS` to resolve an IP address.  After connecting to this IP address, `c2c direct verification` ensures the encoded hash of the servers certificate matches ``hqaceowa9oqbjgz56urj1573ro``.

Address Properties
~~~~~~~~~~~~~~~~~~

The specification of `c2c addresses` is intended to explicitly preserve these properties:

#. It is infeasible for a remote entity to pass a `c2c verification` check for a given address without controlling the identified certificate's private key.
#. Addresses are syntactically valid `DNS` domain names.
#. They will never be valid extant `DNS` domain names (ie: `DNS` will never successfully resolve them.)
#. They can be distinguished from all other domain names precisely by matching the last four characters to ``.c2c``.
#. When they are used in the URL of a browser context (which can resolve and verify them), the layout of `c2c addresses` "works well" with the browser same origin policy:

    * The SOP restrictions of `javascript` are ultimately determined by the certificate.  (**FIXME:** What if Javascript opts into the second level domain which lacks a `hash assertion field`?)
    * The SOP restrictions of `javascript` can be further refined by resolution method.  (**FIXME:** Is this a feature?)
    * JavaScript contexts for a the same website which has been accessed with *both* `c2c` and a standard TLS+PKI https URLs will be isolated from each other by the SOP.

Implementation
==============

The current specification is developing in tandem with a prototypical reference implementation.  This is a set of python libraries implementing the three layers.  Additionally there are some programs to facilitate deploying prototypical `c2c` today.

Libraries
---------

This repository contains separate python packages:

``c2c-verifier`` implements the verification layer for use by `pyOpenSSL` applications.  Note that this library is agnostic about `c2c addresses` and could be used in systems which do not rely on `c2c addresses`.

``c2c-address`` is an address parsing library which is I/O and verification agnostic.

``txc2c`` is a client library built on top of `twisted` and the above two libraries to provide resolution, connection, and verification of `c2c addresses`.

``c2ctool`` is a set of commandline tools:

* A "sniffer" connects to a TLS server and generates an associated `c2c address`.
* A `SOCKS` proxy allows many TCP client applications to use `c2c addresses` without code changes.
