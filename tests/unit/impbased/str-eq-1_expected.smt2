(declare-fun a () String)
(declare-fun b () String)
(declare-fun c () String)
(assert (and (str.prefixof a (str.++ b c)) (str.suffixof a (str.++ b c))))
(check-sat)

