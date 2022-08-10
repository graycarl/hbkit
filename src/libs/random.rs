use rand::Rng;
use rand::distributions::DistString;

pub struct RandomDist {
    source: Vec<char>,
}

impl DistString for RandomDist {
    fn append_string<R: Rng + ?Sized>(&self, rng: &mut R, string: &mut String, len: usize) {
        let source_len = self.source.len();
        for _ in 0..len {
            let x: usize = rng.gen();
            string.push(self.source[x % source_len]);
        }
    }
}

impl RandomDist {
    /// Create a new RandomDist
    /// flags:
    /// - n: 0..9
    /// - a: a..z
    /// - u: A..Z
    /// - f: !@#$%&
    pub fn new<T>(flags: T) -> Result<Self, String> where T: Into<String> {
        let mut s = String::new();
        for f in flags.into().chars() {
            match f {
                'n' => s.push_str("0123456789"),
                'a' => s.push_str("abcdefghijklmnopqrstuvwxyz"),
                'u' => s.push_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                'f' => s.push_str("!@#$%&"),
                'x' => s.push_str("0123456789abcdef"),
                _ => return Err(format!("Unknown flag: '{}'", f))
            }
        }
        return Ok(RandomDist {
            source: s.chars().collect()
        })
    }
}
