(assert (= (str.replace "" "123" "") ""))
(assert (not (= "" "a")))
(assert (= (str.++ "123" "456" (str.replace "" "a" "") "789") (str.substr (str.++ "123456789") 0 10)))
(check-sat)
