(declare-const s1 String)
(declare-const s2 String)
(declare-const s3 String)
(declare-const s4 String)
(assert (str.<= s3 (str.++ s1 s2 s4)))
(assert (= (str.replace "abc" "" "def") "defabc"))
(check-sat)
