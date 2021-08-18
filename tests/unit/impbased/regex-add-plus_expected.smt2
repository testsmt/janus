(assert (str.in_re "a" (re.+ (str.to_re "a"))))
(check-sat)
