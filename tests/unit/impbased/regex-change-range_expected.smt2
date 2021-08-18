(assert (str.in_re "x" (re.range (ite (and (= (str.len "z") 1) (str.<= "z" "t")) "z" "t") "z")))
(assert (str.in_re "1" (re.range (ite (and (= (str.len "t") 1) (str.<= "t" "0")) "t" "0") "3")))
(check-sat)
