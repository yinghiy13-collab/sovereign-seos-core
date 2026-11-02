package seos

import rego.v1

default allow := false

allow if {
    input.scan_type == "STATIC_AST_POLICY_SCAN"
    input.status == "PASS"
    count(input.violations) == 0
    count(input.files_scanned) > 0
    input.commit_sha != ""
}
