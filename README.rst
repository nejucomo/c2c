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

`c2c` clients refer to TLS servers by their certificate's hash using an exceptional pseudo-TLD ``.c2c``.  These pseudo-domains are called `c2c addresses`.  An example c2c address: ``ahqaceowa9oqbjgz56urj1573ro.c2c``

When given such a reference to initiate a connection, TLS verification of the server certificate, they require the server-presented certificate to hash to the given pseudo-domain.

Because the pseudo-domain is not a valid `DNS` name, alternative resolution approaches are possible, the simplest being `immediate resolution` where the pseudo-domains encode IP addresses as well as certificate fingerprints, such as: ``224.154.80.208.ip4.ahqaceowa9oqbjgz56urj1573ro.c2c``

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
