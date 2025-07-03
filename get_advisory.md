# Get Advisory

This is the expected result from using `/api/advisory/1564` endpoint.

Performing a basic **HTTP** request:

```sh
curl -X 'GET' \
  'https://api-ww.cert.orangecyberdefense.com/api/advisory/1564' \
  -H 'accept: application/json' \
  -H 'Authorization: <TOKEN>'
```

An example of this request is present in the provided [`api_usage_example.py`](api_usage_example.py) file

The response should be:

```json
{
  "id": 1564,
  "tdc_id": 651001,
  "title": "Updated - Mandiant reports on sophisticated UNC3886 campaign targeting Juniper routers",
  "severity": 4,
  "categories": [
    "nation-state",
    "vulnerability"
  ],
  "tags": [
    "unc3886"
  ],
  "timestamp_created": "2022-10-03T10:40:11Z",
  "timestamp_updated": "2025-03-13T15:10:48Z",
  "license_agreement": "This advisory has been prepared and is the property of Orange Cyberdefense. Please don't redistribute this content without our agreement.",
  "content_blocks": [
    {
      "id": 4292,
      "advisory": 1564,
      "index": 5,
      "title": "Updated - Mandiant reports on sophisticated UNC3886 campaign targeting Juniper routers",
      "severity": 4,
      "analyst": 2,
      "last_modified_by": 2,
      "categories": [
        "nation-state"
      ],
      "tags": [
        "cve-2025-21590",
        "juniper",
        "tinyshell",
        "unc3886"
      ],
      "advisory_tags": [
        "unc3886"
      ],
      "sources": [
        {
          "id": 11341,
          "type": "external",
          "title": "TinyShell",
          "url": "https://github.com/creaktive/tsh",
          "description": ""
        },
        {
          "id": 11342,
          "type": "external",
          "title": "Mandiant",
          "url": "https://cloud.google.com/blog/topics/threat-intelligence/china-nexus-espionage-targets-juniper-routers?hl=en",
          "description": ""
        },
        {
          "id": 11343,
          "type": "internal",
          "title": "Vulnerability Intelligence Watch",
          "url": "https://portal.cert.orangecyberdefense.com/vulns/92794",
          "description": ""
        }
      ],
      "detection_rules": [
        {
          "id": 51,
          "title": "Yara rule",
          "description": "",
          "content": "rule M_Hunting_PacketEncryptionLayer_1<br>{<br>&nbsp;&nbsp;&nbsp;&nbsp;meta:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;author = \"Mandiant\"<br>&nbsp;&nbsp;&nbsp;&nbsp;strings:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$pel_1 = \"pel_client_init\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$pel_2 = \"pel_server_init\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$pel_3 = \"pel_setup_context\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$pel_4 = \"pel_send_msg\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$pel_5 = \"pel_recv_msg\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$pel_6 = \"pel_send_all\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$pel_7 = \"pel_recv_all\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$pel_8 = \"pel_errno\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$pel_9 = \"pel_context\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$pel_10 = \"pel_ctx\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$pel_11 = \"send_ctx\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$pel_12 = \"recv_ctx\"<br>&nbsp;&nbsp;&nbsp;&nbsp;condition:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4 of ($pel_*)<br>}"
        },
        {
          "id": 52,
          "title": "Yara rule",
          "description": "",
          "content": "rule M_Hunting_TINYSHELL_5<br>{<br>&nbsp;&nbsp;&nbsp;&nbsp;meta:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;author = \"Mandiant\"<br>&nbsp;&nbsp;&nbsp;&nbsp;strings:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$tsh_1 = \"tsh_get_file\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$tsh_2 = \"tsh_put_file\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$tsh_3 = \"tsh_runshell\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$tshd_1 = \"tshd_get_file\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$tshd_2 = \"tshd_put_file\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$tshd_3 = \"tshd_runshell\"<br>&nbsp;&nbsp;&nbsp;&nbsp;condition:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;all of ($tshd_*) or all of ($tsh_*)<br>}"
        },
        {
          "id": 53,
          "title": "Snort/Suricata Rules",
          "description": "",
          "content": "alert udp any any -> any any ( msg:\"M_Backdoor_TINYSHELL_deadbeef_1\"; <br>dsize:>15; content:\"|44 31 3A 14 45 95 6A 73|\"; offset: 0; depth:8; <br>threshold:type limit,track by_src,count 1,seconds 3600; sid:1000000; rev:1; )<br><br>alert udp any any -> any any ( msg:\"M_Backdoor_TINYSHELL_deadbeef_2\"; <br>dsize:>15; content:\"|64 11 1A 34 65 B5 4A 53|\"; offset: 0; depth:8; <br>threshold:type limit,track by_src,count 1,seconds 3600; sid:1000001; rev:1; )<br><br>alert icmp any any -> any any ( msg:\"M_Backdoor_TINYSHELL_uSarguuS62bKRA0J\"; <br>content:\"|f3 d5 e7 f4 e1 f3 f3 d5 b0 b4 e4 cd d4 c7 b6 cc|\"; threshold:type <br>limit,track by_src,count 1,seconds 3600; sid:1000002; rev:1; )<br><br>alert udp any any -> any any ( msg:\"M_Backdoor_TINYSHELL_0b3330c0b41d1ae2\"; <br>dsize:>27; content:\"|c5 c4 ec 4d|\"; offset: 0; depth:4; content:\"|a6 04 ed 83 <br>92 46 ce 40 9a 34 8c 7b 5a d6 e5 0d|\"; offset:12; depth:16; threshold:type <br>limit,track by_src,count 1,seconds 3600; sid:1000003; rev:1; )"
        }
      ],
      "datalake_url": {
        "id": 865,
        "title": "Datalake",
        "description": "",
        "url": "https://datalake.cert.orangecyberdefense.com/gui/search?query_hash=0ca68d191e4a8b4a890ac5f7df95abcd"
      },
      "timestamp_created": "2025-03-13T15:10:48Z",
      "timestamp_updated": "2025-03-13T15:10:48Z",
      "executive_summary": "<p>Mandiant has publicly <a href=\"https://cloud.google.com/blog/topics/threat-intelligence/china-nexus-espionage-targets-juniper-routers?\">detailed</a> a sophisticated campaign carried out by the <strong>Chinese espionage threat actor UNC3886</strong>, known for its advanced operations since 2022 at least. The group is known for its long-term campaigns targeting various critical infrastructure sectors, including via 0-days in virtualization and networking equipment, to maintain privileged access to large-scale networks.</p>\r\n\r\n<p>This latest campaign, from mid-2024, specifically <strong>targeted MX routing equipment products running Juniper Networks&rsquo; OS. </strong>Those had reached their end of life (EoL), making these edge devices particularly vulnerable due to the lack of new security updates and patches.</p>\r\n\r\n<p>The attackers notably exploited the 0-day <strong>CVE-2025-21590 </strong>(<a href=\"https://portal.cert.orangecyberdefense.com/vulns/92794\">link</a> for our Vulnerability intelligence feed customers), affecting the kernel of Juniper Networks&rsquo; JunOS, to deploy backdoors and malware like open source code such as <strong>TINYSHELL</strong>, enabling persistent network penetration. This allowed the group to <strong>establish a long-term, stealth presence</strong> in the affected networks.</p>\r\n\r\n<p>&nbsp;</p>",
      "what_you_will_hear": "",
      "what_it_means": "<p>Tracked by Mandiant since 2022, UNC3886 is an extremely sophisticated Chinese cyberespionage group, which is considered by many CTI researchers as <strong>one of the top China-nexus adversaries.</strong> The group typically uses 0-day vulnerabilities to gain access to victim environments and primarily operate on systems without EDR support.</p>\r\n\r\n<p>In their latest report, Mandiant detailed how UNC3886 compromised around mid 2024 Juniper Networks routers running Junos OS, <strong>specifically MX models that were no longer supported (i.e. EoL).</strong> These became prime targets for threat actors, as they no longer receive patches for newly discovered vulnerabilities.</p>\r\n\r\n<p>The key element of the attack chain was the exploitation of CVE-2025-21590, a remote code execution vulnerability flaw in JunOS. <strong>This vulnerability allows a remote attacker to take full control of a network device without requiring physical access</strong>. The attack can be initiated remotely by exploiting flaws in the management of certain network functions, allowing the attacker to deploy malicious code on the compromised router. Once successfully exploited, the attacker can execute commands remotely and install malware to gain persistent access to the affected system.</p>\r\n\r\n<p>The main malware used in this campaign by UNC3886 is<strong> TINYSHELL, an old lightweight <a href=\"https://github.com/creaktive/tsh\">open-source backdoor in C</a>, </strong>that allowed the attacker to establish a lasting access to the compromised network. The attackers designed at least 6 undocumented TINYSHELL variants designed to be stealthy and hard to detect. The group notably integrated additional features into TINYSHELL to enhance its effectiveness, for example by hiding traces in system logs. Disabling or manipulating logging mechanisms is frequently attempted by attackers to erase evidence of their presence, prevent network administrators from detecting intrusions, thus maintain a discreet and long-lasting control over the compromised devices.</p>\r\n\r\n<p>Additionally, some other modifications allowed UNC3886 to strengthen TINYSHELL&rsquo;s remote control capabilities, facilitating the execution of commands without alerting detection systems.</p>\r\n\r\n<p>The impact of this past campaign is particularly concerning as it <strong>allowed UNC3886 to infiltrate critical communication and other critical infrastructure networks</strong>. The access could provide opportunities for <strong>surveillance, espionage, or even disruption of essential services, depending on the attackers&rsquo; intentions</strong>. Furthermore, this operation also demonstrates that espionage actors linked to China continue to compromise network infrastructures with customized arsenals.</p>\r\n\r\n<p>As mentioned in our previous update, this group is known to exploit a large number of vulnerabilities and uses a wide range of malware for its cyber espionage activities. We leave the risk associated with this advisory 4 out of 5.</p>",
      "what_you_should_do": "<p>We recommend adopting a rigorous approach to network edge devices lifecycle management. This involves implementing continuous monitoring, automating software updates, and replacing swiftly end-of-life solutions. This proactive management ensures that devices in use are always supported by vendors and equipped with the latest security protections.</p>\r\n\r\n<p>Mandiant provided Snort/Suricata and Yara rules to identify specific trafic or files tied to this campaign.</p>\r\n\r\n<p>Orange Cyberdefense&rsquo;s Datalake platform provides access to Indicators of Compromise (<a href=\"https://datalake.cert.orangecyberdefense.com/gui/search?query_hash=0ca68d191e4a8b4a890ac5f7df95abcd\">IoCs</a>) related to this threat, which are automatically fed into our Managed Threat Detection services. This enables proactive hunting for IoCs if you subscribe to our Managed Threat Detection service that includes Threat Hunting. If you would like us to prioritize addressing these IoCs in your next hunt, please make a request through your MTD customer portal or contact your representative.</p>\r\n\r\n<p>Orange Cyberdefense&rsquo;s MTI [protect] service offers the ability to automatically feed network-related IoCs into your security solutions. To learn more about this service and to find out which firewall, proxy, and other vendor solutions are supported, please get in touch with your Orange Cyberdefense Trusted Solutions representative.</p>",
      "what_we_are_doing": "",
      "other": ""
    },
    {
      "id": 3925,
      "advisory": 1564,
      "index": 4,
      "title": "Updated - Mandiant details UNC3886 activities abusing 0-day vulnerabilities, rootkits, and backdoors",
      "severity": 4,
      "analyst": 9,
      "last_modified_by": 9,
      "categories": [
        "nation-state",
        "vulnerability"
      ],
      "tags": [
        "cve-2022-22948",
        "cve-2022-41328",
        "cve-2022-42475",
        "cve-2023-20867",
        "cve-2023-34048",
        "medusa rootkit",
        "mopsled",
        "reptile",
        "riflespine"
      ],
      "advisory_tags": [
        "unc3886"
      ],
      "sources": [
        {
          "id": 9420,
          "type": "external",
          "title": "Mandiant",
          "url": "https://cloud.google.com/blog/topics/threat-intelligence/uncovering-unc3886-espionage-operations?hl=en",
          "description": ""
        },
        {
          "id": 9421,
          "type": "internal",
          "title": "Vulnerability Intelligence Watch",
          "url": "https://portal.cert.orangecyberdefense.com/vulns/58701",
          "description": ""
        },
        {
          "id": 9422,
          "type": "internal",
          "title": "Vulnerability Intelligence Watch",
          "url": "https://portal.cert.orangecyberdefense.com/vulns/56572",
          "description": ""
        },
        {
          "id": 9423,
          "type": "internal",
          "title": "Vulnerability Intelligence Watch",
          "url": "https://portal.cert.orangecyberdefense.com/vulns/50290",
          "description": ""
        },
        {
          "id": 9424,
          "type": "internal",
          "title": "Vulnerability Intelligence Watch",
          "url": "https://portal.cert.orangecyberdefense.com/vulns/55111",
          "description": ""
        },
        {
          "id": 9425,
          "type": "internal",
          "title": "Vulnerability Intelligence Watch",
          "url": "https://portal.cert.orangecyberdefense.com/vulns/53919",
          "description": ""
        }
      ],
      "detection_rules": [],
      "datalake_url": {
        "id": 672,
        "title": "",
        "description": "",
        "url": "https://datalake.cert.orangecyberdefense.com/gui/search?query_hash=0ca68d191e4a8b4a890ac5f7df95abcd"
      },
      "timestamp_created": "2024-06-21T09:04:56Z",
      "timestamp_updated": "2024-06-21T09:06:51Z",
      "executive_summary": "<p>On Tuesday, June 18, Mandiant released a threat intelligence report on the Chinese threat actor <strong>UNC3886</strong>. In January this year, they <a href=\"https://cloud.google.com/blog/topics/threat-intelligence/chinese-vmware-exploitation-since-2021/?hl=en\">had revealed </a>that CVE-2023-34048 affecting VMware had been exploited for over two years by this threat actor (<em>see our previous update</em>). In this new report, Mandiant highlights all known activities of this group. UNC3886 attack chain leads notably to privileged command execution and file transfers within ESXi hypervisors and guest VMs through the following vulnerabilities:</p>\r\n\r\n<ul>\r\n\t<li><strong>CVE-2023-34048</strong> (<em><a href=\"https://portal.cert.orangecyberdefense.com/vulns/58701\">link</a> to the vulnerability advisory for our customers</em>): a 0-day in VMware vCenter Server that allows to execute arbitrary code via specially crafted requests,</li>\r\n\t<li><strong>CVE-2023-20867</strong> (<em><a href=\"https://portal.cert.orangecyberdefense.com/vulns/56572\">link</a> to the vulnerability advisory for our customers</em>): a 0-day in VMware Tools that allows a local attacker with root access on a ESXi host to bypass the authentication of host-to-guest operations,</li>\r\n\t<li><strong>CVE-2022-22948</strong> (<em><a href=\"https://portal.cert.orangecyberdefense.com/vulns/50290\">link</a> to the vulnerability advisory for our customers</em>): a 0-day in VMware vCenter Server and Cloud Foundation that allows a local attacker to gain access to sensitive information,</li>\r\n\t<li><strong>CVE-2022-41328</strong> (<em><a href=\"https://portal.cert.orangecyberdefense.com/vulns/55111\">link</a> to the vulnerability advisory for our customers</em>): a 0-day in Fortinet FortiOS that allows a local attacker to read and write files on the underlying Linux system,</li>\r\n\t<li><strong>CVE-2022-42475</strong> (<em><a href=\"https://portal.cert.orangecyberdefense.com/vulns/53919\">link</a> to the vulnerability advisory for our customers</em>): a vulnerability in Fortinet FortiOS, allowing a remote attacker to execute arbitrary code or commands, abused after its public release.</li>\r\n</ul>\r\n\r\n<p>In addition to these exploited vulnerabilities, Mandiant&rsquo;s teams discovered several tools used by the threat actor, such as:</p>\r\n\r\n<ul>\r\n\t<li><strong>REPTILE</strong>: an open-source rootkit, allowing to establish a backdoor but also to control compromise endpoints by port knocking. Its use can be traced back to at least 2020.</li>\r\n\t<li><strong>MEDUSA</strong>, also an open-source rootkit, that allows, in addition to the basic functionality of a rootkit, to log user credentials and commands, in order to move laterally in the network. SSH credentials were stolen using this tool through a custom SSH server.</li>\r\n\t<li><strong>MOPSLEB</strong>: a backdoor shared between several Chinese groups including the <a href=\"https://portal.cert.orangecyberdefense.com/worldwatch/556546\">APT41</a> nexus, which allows C2 communication via HTTP using a ChaCha20 algorithm to decrypt the configuration file.</li>\r\n\t<li><strong>RIFLESPINE</strong>: a backdoor that encrypts data with an AES algorithm and exfiltrates files via Google Drive.</li>\r\n</ul>\r\n\r\n<p>This APT group thus exhibits a persistent, cautious, evasive, and sophisticated behavior in its malevolent activities, necessitating that we maintain a high threat level associated with it.</p>\r\n\r\n<p>We recommend reducing your attack surface exposure by quickly patching solutions that are heavily exploited by the threat actor, such as the latest vulnerability in VMware. Our <a href=\"https://www.orangecyberdefense.com/global/datasheets/managed-vulnerability-intelligence-watch\">Managed Vulnerability Intelligence</a> services help you triage and prioritise the issues that need immediate attention. Additionally, we offer external asset discovery services to assess the scope of your perimeter, helping to identify unknown domain names, publicly accessible servers, and applications.</p>",
      "what_you_will_hear": "",
      "what_it_means": "<p>We classify this advisory&rsquo;s threat level as 4 out of 5.</p>",
      "what_you_should_do": "<p>Orange Cyberdefense&rsquo;s Datalake platform provides access to Indicators of Compromise (IoCs) related to this threat, which are automatically fed into our Managed Threat Detection services. This enables proactive hunting for IoCs if you subscribe to our Managed Threat Detection service that includes Threat Hunting. If you would like us to prioritize addressing these IoCs in your next hunt, please make a request through your MTD customer portal or contact your representative.</p>\r\n\r\n<p>Orange Cyberdefense&rsquo;s MTI [protect] service offers the ability to automatically feed network-related IoCs into your security solutions. To learn more about this service and to find out which firewall, proxy, and other vendor solutions are supported, please get in touch with your Orange Cyberdefense Trusted Solutions representative.</p>",
      "what_we_are_doing": "",
      "other": ""
    },
    {
      "id": 3417,
      "advisory": 1564,
      "index": 3,
      "title": "Updated - Chinese sophisticated threat actor UNC3886 secretly exploiting CVE-2023-34048 since late 2021",
      "severity": 4,
      "analyst": 3,
      "last_modified_by": 3,
      "categories": [
        "nation-state",
        "vulnerability"
      ],
      "tags": [],
      "advisory_tags": [
        "unc3886"
      ],
      "sources": [
        {
          "id": 7786,
          "type": "external",
          "title": "",
          "url": "https://www.mandiant.com/resources/blog/chinese-vmware-exploitation-since-2021",
          "description": ""
        },
        {
          "id": 7787,
          "type": "external",
          "title": "",
          "url": "https://www.vmware.com/security/advisories/VMSA-2023-0023.html",
          "description": ""
        },
        {
          "id": 7788,
          "type": "internal",
          "title": "Vulnerability Intelligence Watch",
          "url": "https://portal.cert.orangecyberdefense.com/vulns/58701",
          "description": ""
        }
      ],
      "detection_rules": [],
      "datalake_url": null,
      "timestamp_created": "2024-01-22T15:36:48Z",
      "timestamp_updated": "2024-06-19T12:21:23Z",
      "executive_summary": "<p>According to reports from <a href=\"https://www.mandiant.com/resources/blog/chinese-vmware-exploitation-since-2021\"><strong>Mandiant</strong></a> and <strong>VMware</strong>, a critical vulnerability identified in VMware vCenter Server (<strong>CVE-2023-34048, </strong><a href=\"https://portal.cert.orangecyberdefense.com/vulns/58701\">link</a> to the advisory for our Vuln Intelligence clients) has been exploited since late 2021 by a sophisticated Chinese threat actor tracked under the moniker <strong>UNC3886</strong>.<br />\r\n<br />\r\nAs a reminder, this<strong> 0-day</strong> was patched in vCenter Server 6.7U3, 6.5U3, 8.0U1 and VCF 3.x last October 2023. It allows a <strong>remote</strong> attacker to write data outside of the bounds of the memory in the DCE/RPC protocol implementation. A <strong>unauthenticated</strong> attacker could exploit this flaw via specially crafted requests to execute arbitrary code and potentially gain unauthorized access to vCenter systems, enabling further attacks. As a reminder, UNC3886 is known to focus specifically on organizations in the defense, government, telecommunications and technology sectors, notably in the United States.<br />\r\n<br />\r\nMandiant discovered the exploitation of the 0-day after investigating the attacks described in our previous update, involving backdoors they call VirtualPita, VirtualPie and VirtualGate. They observed several crashes corresponding to the exploitation of the 0-day, just before the backdoors were implanted, in several cases related to UNC3886. Threat actors are presumed to have been leveraging the issue possibly since late 2021.<br />\r\n<br />\r\nThe affected environments had preserved log entries, but the &quot;vmdird&quot; core dumps had been intentionally deleted by the attacker to cover its tracks. Furthermore, Mandiant claims that the attack is highly sophisticated, and difficult to identify. We therefore encourage you urgently implement the VMware patch, and hunt for possible sign of compromise, for example in VMware service crash logs (/var/log/vMonCoredumper.log).<br />\r\n<br />\r\nIt is important to note that this threat actor abused <a href=\"https://portal.cert.orangecyberdefense.com/worldwatch/651001\">0-days</a> against VMware or Fortinet products in the past in order to compromise its targets while remaining undetected (see below). This latest operation shows once again that UNC3886 is a skilled actor in the threat landscape.<br />\r\n<br />\r\nThe risk level associated with this threat advisory is thus increased at the level of <strong>4 out of 5</strong>.</p>",
      "what_you_will_hear": "",
      "what_it_means": "",
      "what_you_should_do": "",
      "what_we_are_doing": "",
      "other": ""
    },
    {
      "id": 3414,
      "advisory": 1564,
      "index": 2,
      "title": "Updated - Mandiant says UNC3886 exploits a zero-day vulnerability in VMware ESXi",
      "severity": 3,
      "analyst": 3,
      "last_modified_by": 3,
      "categories": [
        "nation-state",
        "vulnerability"
      ],
      "tags": [
        "cve-2023-20867",
        "cve-2023-34048",
        "unc3886"
      ],
      "advisory_tags": [
        "unc3886"
      ],
      "sources": [
        {
          "id": 7775,
          "type": "external",
          "title": "",
          "url": "https://www.mandiant.com/resources/blog/vmware-esxi-zero-day-bypass",
          "description": ""
        },
        {
          "id": 7776,
          "type": "external",
          "title": "",
          "url": "https://www.vmware.com/security/advisories/VMSA-2023-0013.html",
          "description": ""
        },
        {
          "id": 7777,
          "type": "internal",
          "title": "",
          "url": "https://portal.cert.orangecyberdefense.com/worldwatch/advisory/1578",
          "description": ""
        },
        {
          "id": 7778,
          "type": "internal",
          "title": "Vulnerability Intelligence Watch",
          "url": "https://portal.cert.orangecyberdefense.com/vulns/56572",
          "description": ""
        }
      ],
      "detection_rules": [],
      "datalake_url": {
        "id": 473,
        "title": "",
        "description": "",
        "url": "https://datalake.cert.orangecyberdefense.com/gui/search?query_hash=8555a475181d77015f5a96d9ff30b229"
      },
      "timestamp_created": "2023-06-14T11:11:59Z",
      "timestamp_updated": "2023-06-14T11:11:59Z",
      "executive_summary": "<p>According to a <a href=\"https://www.mandiant.com/resources/blog/vmware-esxi-zero-day-bypass\">report</a> released by <strong>Mandiant</strong>, Chinese threat actor <strong>UNC3886 </strong>exploited a zero-day tracked as <strong><a href=\"https://portal.cert.orangecyberdefense.com/vulns/56572\">CVE-2023-20867</a>, </strong>vulnerability affecting <strong>VMware ESXi</strong> via VMware Tools, to backdoor Windows and Linux virtual machines and <strong>steal data</strong>. VMware Tools is a set of services and modules for enhanced management of guest operating systems. The threat actor allegedly used this authentication bypass flaw to deploy <strong>VirtualPita </strong>and <strong>VirtualPie </strong>backdoors on guest VMs from compromised ESXi hosts where they escalated privileges to root. A third malware strain, <strong>VirtualGate</strong>, acts as a memory-only dropper that deobfuscates second-stage DLL payloads on the hijacked VMs. VMware assessed the flaw as being of <strong>medium severity</strong> because an attacker already needs to have <strong>root access</strong> on an ESXi host.<br />\r\n<br />\r\nIt is worth mentioning that as reported in our initial advisory below, UNC3886 has targeted VMware ESXi servers throughout 2022. Mandiant reported the latest flaw to VMware which released a <a href=\"https://www.vmware.com/security/advisories/VMSA-2023-0013.html\">patch</a> addressing it on June 13. Mandiant found UNC3886 using CVE-2023-20867 as part of a larger and sophisticated attack chain that its researchers have been unraveling over the past several months. The cybersecurity giant added that these attacks were launched against <strong>defense, technology and telecommunications companies</strong>. Mandiant added that the threat actor also adopted previously other advanced techniques such as:<br />\r\n&nbsp;</p>\r\n\r\n<ul>\r\n\t<li>the harvesting of connected ESXi service account credentials on vCenter servers (abusing another older VMware numbered <a href=\"https://portal.cert.orangecyberdefense.com/vulns/50290\">CVE-2023-22948,</a></li>\r\n\t<li>the capabilities of the VMCI socket backdoor.</li>\r\n</ul>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p><br />\r\nMandiant believes this attack chain is very sophisticated, hard to detect and that there are most likely more victims dealing with this threat actor. Thus, we strongly recommend applying the patch released by VMware as soon as possible.<br />\r\n<br />\r\nThe threat level associated with this threat actor will nevertheless remains for now at 3 out of 5.</p>\r\n\r\n<p>&nbsp;</p>",
      "what_you_will_hear": "",
      "what_it_means": "",
      "what_you_should_do": "",
      "what_we_are_doing": "",
      "other": ""
    },
    {
      "id": 3415,
      "advisory": 1564,
      "index": 1,
      "title": "Updated - Suspected Chinese actors behind recent FortiGate zero-day attacks",
      "severity": 3,
      "analyst": 3,
      "last_modified_by": 3,
      "categories": [
        "nation-state"
      ],
      "tags": [
        "cve-2022-41328"
      ],
      "advisory_tags": [
        "unc3886"
      ],
      "sources": [
        {
          "id": 7779,
          "type": "external",
          "title": "",
          "url": "https://www.mandiant.com/resources/blog/fortinet-malware-ecosystem",
          "description": ""
        },
        {
          "id": 7780,
          "type": "internal",
          "title": "",
          "url": "https://portal.cert.orangecyberdefense.com/worldwatch/advisory/1578",
          "description": ""
        },
        {
          "id": 7781,
          "type": "internal",
          "title": "Vulnerability Intelligence Watch",
          "url": "https://portal.cert.orangecyberdefense.com/vulns/55111",
          "description": ""
        }
      ],
      "detection_rules": [],
      "datalake_url": {
        "id": 474,
        "title": "",
        "description": "",
        "url": "https://datalake.cert.orangecyberdefense.com/gui/search?query_hash=8555a475181d77015f5a96d9ff30b229"
      },
      "timestamp_created": "2023-03-17T12:50:10Z",
      "timestamp_updated": "2024-06-19T12:20:15Z",
      "executive_summary": "<p>Shortly after Fortinet disclosed that <a href=\"https://portal.cert.orangecyberdefense.com/vulns/55111\">CVE-2022-41328</a>, a medium-severity path traversal vulnerability in FortiOS, had been exploited by unknown sophisticated threat actors targeting governmental entities (as discussed in this <a href=\"https://portal.cert.orangecyberdefense.com/worldwatch/696477\">World Watch alert</a>), Mandiant released a detailed report attributing this campaign to <strong>UNC3886</strong>.<br />\r\n<br />\r\nAccording to Mandiant, the campaign started in mid-2022, and the threat actor infected multiple Fortinet solutions with malware, including FortiGate (firewall), FortiManager (centralized management solution), and FortiAnalyzer (log management, analytics and reporting). Furthermore, the hackers also deployed the <strong>VirtualPita </strong>and <strong>VirtualPie </strong>backdoors (as discussed in the previous update) on VMWare ESXI servers during the campaign.<br />\r\n<br />\r\nAfter the attackers initially gained access to an exposed FortiManager instance, they modified legitimate Python code to implement a custom backdoor dubbed <strong>ThinCrust </strong>to FortiManager and FortiAnalyzer. ThinCrust is a Python-based backdoor appended to a legitimate web framework file. The backdoor disguises its communications as legitimate API calls by including an additional malicious API call. The backdoor allows the attacker to execute commands, write files to disk and read files from disk depending on the cookies provided in the request.<br />\r\n<br />\r\nAfter establishing persistence on FortiManager and FortiAnalyzer, the threat actor then modified FortiManager scripts to deploy the <strong>CastleTap </strong>backdoor across all FortiGate devices by exploiting CVE-2022-41328. This vulnerability allowed the threat actor to overwrite system binaries, and then use legitimate commands that relied on those binaries to achieve code executon. UNC3886 then finally deployed an additional malicious file containing CastleTap. This passive backdoor examines received ICMP packets looking for a hardcoded string in the payload of an ICMP echo request packet (ping packet). After detecting this activation string, CastleTap parses C2 information from the packet payload and connects to it over SSL. The backdoor then offers standard functionality of uploading/downloading files and command execution.<br />\r\n<br />\r\nThe threat actor also connected to the ESXi servers via the compromised Fortinet devices to install the VirtualPita and VirtualPie backdoors, which allowed them to execute commands on guest virtual machines.<br />\r\n<br />\r\nAfter network Access Control Lists (ACL) were put in place to restrict traffic to the FortiManager instance, the attacker deployed an additional network traffic redirection malware dubbed <strong>TableFlip </strong>and a reverse shell backdoor dubbed <strong>Reptile </strong>on the FortiManager to bypass the ACL. This gave the threat actor the ability to create their own traffic redirection rules, allowing them to bypass any traffic redirection rule put in place to block their access. Then, the threat actor configured redirection rules to forward incoming malicious traffic from the internet to the Reptile backdoor. Reptile is a variant of a publicly available Linux kernel module rootkit which listens for a hardcoded strings on incoming packets and opens a reverse shell to the C2 IP extracted from the packet payload data.<br />\r\n<br />\r\nFinally, Mandiant also observed several anti-forensic commands executed by the threat actor in order to cover their tracks and remove suspicious log lines.<br />\r\n<br />\r\nDue to the high sophistication of this campaign, which included deploying multiple custom stealthy backdoors, exploiting a zero-day and manipulating firewall firmware, we are increasing the severity level associated to this threat to 3 out of 5.</p>",
      "what_you_will_hear": "",
      "what_it_means": "",
      "what_you_should_do": "",
      "what_we_are_doing": "",
      "other": ""
    },
    {
      "id": 3413,
      "advisory": 1564,
      "index": 0,
      "title": "UNC3886 backdoors ESXi servers to hijack virtual machines",
      "severity": 3,
      "analyst": 3,
      "last_modified_by": 3,
      "categories": [
        "nation-state"
      ],
      "tags": [
        "unc3886"
      ],
      "advisory_tags": [
        "unc3886"
      ],
      "sources": [
        {
          "id": 7772,
          "type": "external",
          "title": "",
          "url": "https://www.mandiant.com/resources/blog/esxi-hypervisors-malware-persistence",
          "description": ""
        },
        {
          "id": 7773,
          "type": "external",
          "title": "",
          "url": "https://www.mandiant.com/resources/blog/esxi-hypervisors-detection-hardening",
          "description": ""
        },
        {
          "id": 7774,
          "type": "external",
          "title": "",
          "url": "https://core.vmware.com/vsphere-esxi-mandiant-malware-persistence",
          "description": ""
        }
      ],
      "detection_rules": [],
      "datalake_url": {
        "id": 472,
        "title": "",
        "description": "",
        "url": "https://datalake.cert.orangecyberdefense.com/gui/search?query_hash=8555a475181d77015f5a96d9ff30b229"
      },
      "timestamp_created": "2022-09-30T13:29:49Z",
      "timestamp_updated": "2024-06-19T12:16:06Z",
      "executive_summary": "<p>Researchers from Mandiant <a href=\"https://www.mandiant.com/resources/blog/esxi-hypervisors-malware-persistence\">uncovered</a> a <strong>novel malware ecosystem </strong>impacting VMware ESXi, Linux vCenter servers, and Windows virtual machines. It enables a threat actor to <strong>maintain persistent administrative access </strong>to the hypervisor, send commands that will be routed to the guest VM for execution, transfer files, tamper with logging services and execute arbitrary commands from one VM to another. This is achieved by using malicious vSphere Installation Bundles (VIBs) to install multiple backdoors across ESXi hypervisors. It is important to note that this is not an unauthenticated nor remote vulnerability, because <strong>prior administrative access </strong>to the ESXi hypervisor is required in order to deploy the backdoor.Mandiant could not attribute this malicious activity to any known threat actor yet, so it tracks it separately as <strong>UNC3886</strong>. Given the highly targeted and evasive nature of the intrusion, the researchers suspect that the threat actor&#39;s motivation is <strong>cyberespionage</strong> related, and that the group has ties with <strong>China</strong>.</p>",
      "what_you_will_hear": "<p>New malware backdoors ESXi servers to hijack virtual machines.</p>",
      "what_it_means": "<p>During an intrusion investigated earlier this year, Mandiant researchers identified two new malware families installed through malicious VIBs, dubbed <strong>VirtualPita </strong>and <strong>VirtualPie</strong>.<br />\r\nVirtualPita is a 64-bit passive backdoor that creates a listener on a hardcoded port number on a compromised VMware ESXi server. It often uses legitimate VMware service names and ports to masquerade as a legitimate service. The backdoor supports the following features:</p>\r\n\r\n<ul>\r\n\t<li>arbitrary command execution,</li>\r\n\t<li>file upload and download,</li>\r\n\t<li>and the ability to start and stop the VMware&#39;s logging daemon &quot;vmsyslogd&quot;.</li>\r\n</ul>\r\n\r\n<p><br />\r\nDuring arbitrary command execution, the malware sets the environment variable HISTFILE to 0, to instruct the system to not keep any logs of the Bash commands executed. During the investigation, the researchers found 2 additional VirtualPita samples listening on TCP port 7475, that persist on the system using an &quot;init.d&quot; startup service on Linux vCenter, disguised as a legitimate binary named &quot;ksmd&quot;.<br />\r\nVirtualPie is a lightweight Python-based backdoor that spawns an IPv6 listener on a hardcoded port on a VMware ESXi server. It supports:</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<ul>\r\n\t<li>arbitrary command execution,</li>\r\n\t<li>file transfer</li>\r\n\t<li>and reverse shell capabilities.</li>\r\n</ul>\r\n\r\n<p><br />\r\nThis backdoor uses a custom protocol for communication, which is encrypted using a RC4 key.<br />\r\nFinally, in guest VMs running Windows under such an infected hypervisor, the researchers found another malware, dubbed VirtualGate, which includes a memory-only dropper responsible for deobfuscating a second-stage DLL payload.<br />\r\nAs for post-exploitation, the attacker executed commands observed by Mandiant focused on enumeration and file compression across the system and connected file shares, as well as credential harvesting using MiniDump (a tool which dumps process memory and search for cleartext credentials).We have attributed a risk-level of 1 to this alert as these malware strains, although stealthy, are mainly used in targeted cyber espionage campaigns and require to have administrative rights to be deployed.</p>\r\n\r\n<p>&nbsp;</p>",
      "what_you_should_do": "<p>On a separate <a href=\"https://www.mandiant.com/resources/blog/esxi-hypervisors-detection-hardening\">blog post</a>, Mandiant describes ESXi detection methodologies, which involve dumping memory processes and performing Yara scans, as well as provides guidance on how to harden hypervisors to minimize the attack surface of ESXi hosts. VMware has also released <a href=\"https://core.vmware.com/vsphere-esxi-mandiant-malware-persistence\">additional information</a> on protecting vSphere from targeted malware.Some Yara rules provided by Mandiant are available in the Appendices. IoCs from the malware strains are also available in the original article and in our Datalake platform used by our Managed Threat Detection services. These can be proactively added and hunted for in your security solutions (SIEM, NGFW, EDR, etc.). Orange Cyberdefense can orchestrate the automatic feeding of such network-related IOCs in your firewall equipments using our &quot;Managed Threat Intelligence - protect&quot; service.</p>",
      "what_we_are_doing": "",
      "other": ""
    }
  ]
}
```