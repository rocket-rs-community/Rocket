# `dyn_templates` [![ci.svg]][ci] [![crates.io]][crate] [![docs.svg]][crate docs]

[crates.io]: https://img.shields.io/crates/v/rocket_dyn_templates-community.svg
[crate]: https://crates.io/crates/rocket_dyn_templates-community
[docs.svg]: https://img.shields.io/badge/web-master-red.svg?style=flat&label=docs&colorB=d33847
[crate docs]: https://docs.rs/rocket_dyn_templates-community/latest/rocket_dyn_templates_community/
[ci.svg]: https://github.com/rocket-ws-community/Rocket/workflows/CI/badge.svg
[ci]: https://github.com/rocket-ws-community/Rocket/actions

This crate adds support for dynamic template rendering to Rocket. It
automatically discovers templates, provides a `Responder` to render templates,
and automatically reloads templates when compiled in debug mode. It supports [Handlebars], [Tera] and [MiniJinja].

[Tera]: https://docs.rs/crate/tera/1
[Handlebars]: https://docs.rs/crate/handlebars/5
[MiniJinja]: https://docs.rs/crate/minijinja/2.0.1

# Usage

  1. Enable the `rocket_dyn_templates` feature corresponding to your templating
     engine(s) of choice:

     ```toml
     [dependencies.rocket_dyn_templates]
     package = "rocket_dyn_templates-community"
     version = "0.3.2"
     features = ["handlebars", "tera", "minijinja"]
     ```

  1. Write your template files in Handlebars (`.hbs`) and/or Tera (`.tera`) in
     the configurable `template_dir` directory (default:
     `{rocket_root}/templates`).

  2. Attach `Template::fairing()` and return a `Template` using
     `Template::render()`, supplying the name of the template file **minus the
     last two extensions**:

     ```rust
     use rocket_dyn_templates::{Template, context};

     #[get("/")]
     fn index() -> Template {
         Template::render("template-name", context! { field: "value" })
     }

     #[launch]
     fn rocket() -> _ {
         rocket::build().attach(Template::fairing())
     }
     ```

See the [crate docs] for full details.
