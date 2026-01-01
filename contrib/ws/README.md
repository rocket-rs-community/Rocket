# `ws` [![ci.svg]][ci] [![crates.io]][crate] [![docs.svg]][crate docs]

[crates.io]: https://img.shields.io/crates/v/rocket_ws-community.svg
[crate]: https://crates.io/crates/rocket_ws-community
[docs.svg]: https://img.shields.io/badge/web-master-red.svg?style=flat&label=docs&colorB=d33847
[crate docs]: https://docs.rs/rocket_ws-community/latest/rocket_ws_community/
[ci.svg]: https://github.com/rocket-rs-community/Rocket/workflows/CI/badge.svg
[ci]: https://github.com/rocket-rs-community/Rocket/actions

This crate provides WebSocket support for Rocket via integration with Rocket's
[connection upgrades] API.

# Usage

  1. Depend on `rocket_ws`, renamed here to `ws`:

     ```toml
     [dependencies]
     ws = { package = "rocket_ws-community", version = "0.1.2" }
     ```

   2. Use it!

      ```rust
      #[get("/echo")]
      fn echo_stream(ws: ws::WebSocket) -> ws::Stream!['static] {
          ws::Stream! { ws =>
              for await message in ws {
                  yield message?;
              }
          }
      }
      ```

See the [crate docs] for full details.
