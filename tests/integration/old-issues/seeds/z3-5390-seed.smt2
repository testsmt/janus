(declare-const a String)
(declare-const x RegLan)
(assert (str.in_re a (re.+ x)))
(check-sat)
