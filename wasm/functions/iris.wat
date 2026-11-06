;; Dokumentasi (versi teks) dari iris.wasm. Model: Logistic Regression Iris.
;; Memori linear berisi 3 kelas x (4 bobot + 1 bias), masing-masing i32 little-endian.
;; Input = ukuran dalam cm x 10 (mis. 5.1 cm -> 51). Output classify: 0=setosa 1=versicolor 2=virginica
(module
  (memory (export "memory") 1)
  (data (i32.const 0) "\5e\fd\ff\ff\3a\07\00\00\62\f0\ff\ff\87\f8\ff\ff\a9\50\02\00\ea\03\00\00\11\00\00\00\4f\fe\ff\ff\1f\f8\ff\ff\15\60\00\00\b8\fe\ff\ff\b5\f8\ff\ff\4f\11\00\00\5a\0f\00\00\42\4f\fd\ff")

  (func $score (export "score") (param $k i32) (param $a i32) (param $b i32) (param $c i32) (param $d i32) (result i32)
    (local $p i32)
    (local.set $p (i32.mul (local.get $k) (i32.const 20)))
    (i32.add
      (i32.add
        (i32.add
          (i32.add
            (i32.mul (i32.load (local.get $p)) (local.get $a))
            (i32.mul (i32.load offset=4 (local.get $p)) (local.get $b)))
          (i32.mul (i32.load offset=8 (local.get $p)) (local.get $c)))
        (i32.mul (i32.load offset=12 (local.get $p)) (local.get $d)))
      (i32.load offset=16 (local.get $p))))

  (func (export "classify") (param $a i32) (param $b i32) (param $c i32) (param $d i32) (result i32)
    (local $s0 i32) (local $s1 i32) (local $s2 i32) (local $best i32) (local $m i32)
    (local.set $s0 (call $score (i32.const 0) (local.get $a) (local.get $b) (local.get $c) (local.get $d)))
    (local.set $s1 (call $score (i32.const 1) (local.get $a) (local.get $b) (local.get $c) (local.get $d)))
    (local.set $s2 (call $score (i32.const 2) (local.get $a) (local.get $b) (local.get $c) (local.get $d)))
    (local.set $best (i32.const 0))
    (local.set $m (local.get $s0))
    (if (i32.gt_s (local.get $s1) (local.get $m))
      (then (local.set $best (i32.const 1)) (local.set $m (local.get $s1))))
    (if (i32.gt_s (local.get $s2) (local.get $m))
      (then (local.set $best (i32.const 2))))
    (local.get $best))

  (func (export "work") (param $n i32) (result i32)
    (local $i i32) (local $acc i32)
    (block $done
      (loop $l
        (br_if $done (i32.ge_u (local.get $i) (local.get $n)))
        (local.set $acc (i32.add (local.get $acc) (i32.mul (local.get $i) (i32.const 3))))
        (local.set $i (i32.add (local.get $i) (i32.const 1)))
        (br $l)))
    (local.get $acc))

  (func (export "spin") (loop $l (br $l)))
)
