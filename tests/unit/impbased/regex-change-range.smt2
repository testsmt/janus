(assert (str.in_re "x" (re.range "t" "z")))
(assert (str.in_re "1" (re.range "0" "3")))
(check-sat)
