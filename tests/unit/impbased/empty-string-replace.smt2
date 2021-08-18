(assert (= "" ""))
(assert (not (= (str.replace "" "abc" "") "a")))
(assert (= (str.++ "123" "456" "" "789") (str.substr (str.++ "123456789") 0 10)))
(check-sat)
