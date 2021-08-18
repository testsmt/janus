(assert (let ((y (forall ((x Bool)) (let ((y x)) (or y (not y)))))) (or y (not y))))
(check-sat)
