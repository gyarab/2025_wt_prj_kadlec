from ninja import NinjaAPI, ModelSchema, Schema
from typing import List
from .models import Auto, Rezervace, Uzivatel
import datetime

api = NinjaAPI()

class MessageSchema(Schema):
    message: str

class AutoSchema(ModelSchema):
    class Meta:
        model = Auto
        model_fields = "__all__"

class AutoSchemaIn(ModelSchema):
    class Meta:
        model = Auto
        exclude = ["id"]

class AutoListingSchema(Schema):
    count: int
    results: List[AutoSchema]

@api.get("/auto", response=AutoListingSchema, tags=["Auto"])
def get_auta(request):
    auta = Auto.objects.all()
    return {
        "count": len(auta),
        "results": list(auta)
    }

@api.get("/auto/{auto_id}", response={200: AutoSchema, 404: MessageSchema}, tags=["Auto"])
def get_auto(request, auto_id: int):
    try:
        auto = Auto.objects.get(id=auto_id)
        return 200, auto
    except Auto.DoesNotExist:
        return 404, {"message": "Auto nenalezeno"}

@api.post("/auto", response={201: AutoSchema}, tags=["Auto"])
def create_auto(request, data: AutoSchemaIn):
    auto = Auto.objects.create(**data.dict())
    return 201, auto

@api.put("/auto/{auto_id}", response={200: AutoSchema, 404: MessageSchema}, tags=["Auto"])
def update_auto(request, auto_id: int, data: AutoSchemaIn):
    try:
        auto = Auto.objects.get(id=auto_id)
        for attr, value in data.dict().items():
            setattr(auto, attr, value)
        auto.save()
        return 200, auto
    except Auto.DoesNotExist:
        return 404, {"message": "Auto nenalezeno"}

class RezervaceSchema(ModelSchema):
    class Meta:
        model = Rezervace
        model_fields = "__all__"
        exclude = ["uzivatel", "auto"]
    uzivatel: str | None
    auto: str | None

class RezervaceListingSchema(Schema):
    count: int
    results: List[RezervaceSchema]

class RezervaceSchemaIn(Schema):
    uzivatel_id: int
    auto_id: int
    datum_vyzvednuti: datetime.date
    misto_vraceni: str
    typ_pojisteni: str
    stav: str
@api.get("/rezervace", response=RezervaceListingSchema, tags=["Rezervace"])
def get_rezervace_list(request):
    rezervace = Rezervace.objects.select_related('uzivatel', 'auto').all()
    out = []
    for r in rezervace:
        out.append({
            "id": r.id,
            "datum_vyzvednuti": str(r.datum_vyzvednuti) if r.datum_vyzvednuti else None,
            "misto_vraceni": r.misto_vraceni,
            "typ_pojisteni": r.typ_pojisteni,
            "stav": r.stav,
            "uzivatel": r.uzivatel.jmeno if r.uzivatel else None,
            "auto": r.auto.znacka_a_model if r.auto else None
        })
    return {
        "count": len(out),
        "results": out
    }

@api.get("/rezervace/{rezervace_id}", response={200: RezervaceSchema, 404: MessageSchema}, tags=["Rezervace"])
def get_rezervace_detail(request, rezervace_id: int):
    try:
        r = Rezervace.objects.select_related('uzivatel', 'auto').get(id=rezervace_id)
        return 200, {
            "id": r.id,
            "datum_vyzvednuti": str(r.datum_vyzvednuti) if r.datum_vyzvednuti else None,
            "misto_vraceni": r.misto_vraceni,
            "typ_pojisteni": r.typ_pojisteni,
            "stav": r.stav,
            "uzivatel": r.uzivatel.jmeno if r.uzivatel else None,
            "auto": r.auto.znacka_a_model if r.auto else None
        }
    except Rezervace.DoesNotExist:
        return 404, {"message": "Rezervace nenalezena"}

@api.post("/rezervace", response={201: RezervaceSchema, 404: MessageSchema}, tags=["Rezervace"])
def create_rezervace(request, data: RezervaceSchemaIn):
    try:
        uzivatel = Uzivatel.objects.get(id=data.uzivatel_id)
        auto = Auto.objects.get(id=data.auto_id)
    except (Uzivatel.DoesNotExist, Auto.DoesNotExist):
        return 404, {"message": "Uživatel nebo auto nenalezeno"}
        
    r = Rezervace.objects.create(
        uzivatel=uzivatel,
        auto=auto,
        datum_vyzvednuti=data.datum_vyzvednuti,
        misto_vraceni=data.misto_vraceni,
        typ_pojisteni=data.typ_pojisteni,
        stav=data.stav
    )
    return 201, {
        "id": r.id,
        "datum_vyzvednuti": str(r.datum_vyzvednuti) if r.datum_vyzvednuti else None,
        "misto_vraceni": r.misto_vraceni,
        "typ_pojisteni": r.typ_pojisteni,
        "stav": r.stav,
        "uzivatel": r.uzivatel.jmeno if r.uzivatel else None,
        "auto": r.auto.znacka_a_model if r.auto else None
    }

@api.put("/rezervace/{rezervace_id}", response={200: RezervaceSchema, 404: MessageSchema}, tags=["Rezervace"])
def update_rezervace(request, rezervace_id: int, data: RezervaceSchemaIn):
    try:
        r = Rezervace.objects.get(id=rezervace_id)
    except Rezervace.DoesNotExist:
        return 404, {"message": "Rezervace nenalezena"}
        
    try:
        uzivatel = Uzivatel.objects.get(id=data.uzivatel_id)
        auto = Auto.objects.get(id=data.auto_id)
    except (Uzivatel.DoesNotExist, Auto.DoesNotExist):
        return 404, {"message": "Uživatel nebo auto nenalezeno"}
        
    r.uzivatel = uzivatel
    r.auto = auto
    r.datum_vyzvednuti = data.datum_vyzvednuti
    r.misto_vraceni = data.misto_vraceni
    r.typ_pojisteni = data.typ_pojisteni
    r.stav = data.stav
    r.save()
    
    return 200, {
        "id": r.id,
        "datum_vyzvednuti": str(r.datum_vyzvednuti) if r.datum_vyzvednuti else None,
        "misto_vraceni": r.misto_vraceni,
        "typ_pojisteni": r.typ_pojisteni,
        "stav": r.stav,
        "uzivatel": r.uzivatel.jmeno if r.uzivatel else None,
        "auto": r.auto.znacka_a_model if r.auto else None
    }
