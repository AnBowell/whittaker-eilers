use whittaker_eilers::eye;

#[test]
pub fn test_eye() {
    let x = eye(100);

    println!("x: {:?}", x);
}
