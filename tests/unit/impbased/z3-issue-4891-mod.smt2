(declare-fun a () Int)
(declare-fun b () Int)
(declare-fun c () Int)
(declare-fun d () Int)
(declare-fun e () Int)
(declare-fun f () Int)
(declare-fun g () Int)
(declare-fun h () Int)
(assert (= g (* g d) (+ (- 1) (* d h) a) (* a (- 1 g)) (+ f (* d g c) (- e) (* (* g b) 1)) 0))
(assert (>= d (+ f (* h c) (- e) (- (* d b)) (* g b)) (+ e d (- (+ d h)) (- (* h h c))) 0))
(assert (> (+ (mod d b) g) 0 (* d c)))
(assert (>= d 0))
(assert (>= g 0))
(assert (>= h f))
(check-sat)