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

Example Use Case
~~~~~~~~~~~~~~~~

Suppose a large network service uses a VPS system to rapidly deploy debian-based virtual machines.  The service has an internal package repository for these VPS guests.  The guests may be initially launched with a `c2c address` in the `apt` ``sources.list`` file.  After a guest is launched, package updates can use the standard `apt-get` upgrade mechanism.

Because the service uses `c2c addresses`, there is no need to manage `DNS` entries or CA signatures on the internal package repository host, saving cost and complexity.  Because the ``sources.list`` file is managed by devops engineers and rarely altered, there is little need for human-meaningful names (similar to an ``~/.ssh/authorized_keys`` file, for example).

Redeployment of the guests is low cost, so in the event that the package repository certificate must be rotated, a new guest deployment cycle can upgrade the `c2c addresses` used by ``apt``.  This is an example of a custom, feasible key rotation mechanism, even though `c2c` itself is agnostic about key management.

Assume that the VPS deployment process and the source of the ``sources.list`` file are not compromised by an attacker, and also that `apt` package signing is disabled (which is hopefully rare in modern times).  In the traditional case of securing communication with the package repository by ``https`` URLs, a compromised CA can enable an active interception attack (aka "man in the middle") to inject malicious packages.  By contrast, after the `c2c`-based VPS deployment is complete, an attacker cannot execute such an interception attack, and must instead compromise something aside from TLS authentication (eg: the repository or installing VPS hosts, or other areas of the TLS protocol)


Three Conventions
=================

`c2c` is composed of three conventions
