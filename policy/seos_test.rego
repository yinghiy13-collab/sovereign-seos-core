package seos

import rego.v1

test_allow_valid_scan if {
    allow with input as {
        "scan_type": "STATIC_AST_POLICY_SCAN",
        "status": "PASS",
        "violations": [],
        "files_scanned": ["main.py"],
        "commit_sha": "abc1234"
    }
}

test_deny_violations if {
    not allow with input as {
        "scan_type": "STATIC_AST_POLICY_SCAN",
        "status": "PASS",
        "violations": [{"issue": "eval found"}],
        "files_scanned": ["main.py"],
        "commit_sha": "abc1234"
    }
}

test_deny_empty_scan if {
    not allow with input as {
        "scan_type": "STATIC_AST_POLICY_SCAN",
        "status": "PASS",
        "violations": [],
        "files_scanned": [],
        "commit_sha": "abc1234"
    }
}
