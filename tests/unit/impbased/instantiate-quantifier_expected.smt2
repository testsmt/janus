(assert (or
	(exists ((b Bool)) (and b (not b)))
	(not (exists ((b Bool)) (and b (not b))))
))
(assert (not (and
	(not (exists ((b Bool)) (and b (not b))))
	(not (not (exists ((b Bool)) (and b (not b)))))
)))

(check-sat)
