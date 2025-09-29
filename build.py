#!/usr/bin/env python3
# Build Promtmix static site into /public then copy files to repo root as needed.
import os, json, shutil, datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

BASE = Path(__file__).resolve().parent.parent
SRC = BASE / "src"
PUBLIC = BASE / "public"

config = json.load(open(BASE/"config.json", "r", encoding="utf-8"))

env = Environment(loader=FileSystemLoader(str(SRC/"templates")), autoescape=select_autoescape(['html']))
def render(tpl, **ctx):
    ctx.setdefault("adsense_client", config["adsense_client"])
    ctx.setdefault("year", datetime.datetime.utcnow().year)
    ctx.setdefault("build_time", datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"))
    return env.get_template(tpl).render(**ctx)

# Read simple list of converters from json pre-exported by initial build
converters = json.load(open(SRC/"data"/"converters.json","r",encoding="utf-8"))

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def copy_assets():
    out = PUBLIC/"assets"
    out.mkdir(parents=True, exist_ok=True)
    for f in (SRC/"assets").glob("*.*"):
        shutil.copy2(f, out/f.name)

def build():
    PUBLIC.mkdir(exist_ok=True, parents=True)
    # Index
    write(PUBLIC/"index.html", render("index.html",
        title="Fast, minimalist tools",
        description="Converters, logistics calculators and nutrition tools.",
        canonical=config["base_url"]+"/",
        section="converters"))
    write(PUBLIC/"about.html", render("about.html",
        title="About",
        description="About Promtmix",
        canonical=config["base_url"]+"/about.html",
        section="converters"))

    copy_assets()

    # Converters
    write(PUBLIC/"converters"/"index.html", render("converters_index.html",
        title="Converters",
        description="Unit converters.",
        canonical=config["base_url"]+"/converters/",
        section="converters",
        converters=[{"label":c["label"],"desc":c["desc"],"url":f"/promtmix/converters/{c['slug']}.html"} for c in converters]))
    for c in converters:
        write(PUBLIC/"converters"/f"{c['slug']}.html", render("converter.html",
            title=c["label"],
            description=c["desc"],
            canonical=f"{config['base_url']}/converters/{c['slug']}.html",
            section="converters",
            label=c["label"], desc=c["desc"],
            from_unit=c["from"], to_unit=c["to"],
            default_value=c["preset"][0],
            presets=c["preset"], formula_js=c["formula_js"], formula_desc=c["formula_desc"],
            gear_query=c["gear_query"]))

    # Logistics
    write(PUBLIC/"logistics"/"index.html", render("logistics_index.html",
        title="Logistics calculators",
        description="Box volume and dimensional weight calculators for UPS, FedEx, DHL, USPS.",
        canonical=config["base_url"]+"/logistics/",
        section="logistics"))
    write(PUBLIC/"logistics"/"box-volume.html", render("box_volume.html",
        title="Box volume",
        description="Calculate box volume.",
        canonical=config["base_url"]+"/logistics/box-volume.html",
        section="logistics"))
    write(PUBLIC/"logistics"/"dim-weight.html", render("dim_weight.html",
        title="Dimensional weight",
        description="Estimate dimensional weight.",
        canonical=config["base_url"]+"/logistics/dim-weight.html",
        section="logistics"))

    # Nutrition
    write(PUBLIC/"nutrition"/"index.html", render("nutrition_index.html",
        title="Nutrition tools",
        description="BMI, BMR/TDEE and macros.",
        canonical=config["base_url"]+"/nutrition/",
        section="nutrition"))
    write(PUBLIC/"nutrition"/"bmi.html", render("bmi.html",
        title="BMI calculator",
        description="BMI calculator metric/imperial.",
        canonical=config["base_url"]+"/nutrition/bmi.html",
        section="nutrition"))
    write(PUBLIC/"nutrition"/"bmr.html", render("bmr.html",
        title="BMR & TDEE calculator",
        description="Mifflin-St Jeor BMR and daily energy.",
        canonical=config["base_url"]+"/nutrition/bmr.html",
        section="nutrition"))
    write(PUBLIC/"nutrition"/"macros.html", render("macros.html",
        title="Macro splits",
        description="Convert calories into grams of protein/carbs/fat.",
        canonical=config["base_url"]+"/nutrition/macros.html",
        section="nutrition"))

    # Robots & sitemap
    urls = [
        f"{config['base_url']}/",
        f"{config['base_url']}/about.html",
        f"{config['base_url']}/converters/",
        f"{config['base_url']}/logistics/",
        f"{config['base_url']}/nutrition/",
        f"{config['base_url']}/logistics/box-volume.html",
        f"{config['base_url']}/logistics/dim-weight.html",
        f"{config['base_url']}/nutrition/bmi.html",
        f"{config['base_url']}/nutrition/bmr.html",
        f"{config['base_url']}/nutrition/macros.html",
    ] + [f"{config['base_url']}/converters/{c['slug']}.html" for c in converters]

    write(PUBLIC/"robots.txt", "User-agent: *\\nAllow: /\\nSitemap: "+config["base_url"]+"/sitemap.xml\\n")
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    sm = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"<url><loc>{u}</loc><lastmod>{now}</lastmod><changefreq>weekly</changefreq></url>")
    sm.append("</urlset>")
    write(PUBLIC/"sitemap.xml", "\\n".join(sm))

    # Copy everything from /public into repo root (for GitHub Pages root deploy)
    for item in PUBLIC.glob("**/*"):
        if item.is_file():
            dest = BASE / item.relative_to(PUBLIC)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)

if __name__ == "__main__":
    # Save converters data file for consistency
    import json
    json.dump(converters, open(SRC/"data"/"converters.json","w",encoding="utf-8"), indent=2)
    build()
