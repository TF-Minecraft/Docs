app/lib/map/editor/countyAssignment.test.ts(49,48): error TS2345: Argument of type '{ COUNTY_1: { name: string; provinces: number[]; }; COUNTY_2: { name: string; provinces: number[]; }; }' is not assignable to parameter of type 'TitleDraft'.
  Property 'COUNTY_1' is incompatible with index signature.
    Property 'rgb' is missing in type '{ name: string; provinces: number[]; }' but required in type 'EditorTitleEntry'.
app/lib/map/editor/countyAssignment.test.ts(50,49): error TS2345: Argument of type '{ COUNTY_1: { name: string; provinces: number[]; }; COUNTY_2: { name: string; provinces: number[]; }; }' is not assignable to parameter of type 'TitleDraft'.
  Property 'COUNTY_1' is incompatible with index signature.
    Property 'rgb' is missing in type '{ name: string; provinces: number[]; }' but required in type 'EditorTitleEntry'.
app/lib/map/editor/duchyAssignment.test.ts(40,55): error TS2345: Argument of type '{ DUCHY_1: { name: string; titles: string[]; }; DUCHY_2: { name: string; titles: string[]; }; }' is not assignable to parameter of type 'TitleDraft'.
  Property 'DUCHY_1' is incompatible with index signature.
    Property 'rgb' is missing in type '{ name: string; titles: string[]; }' but required in type 'EditorTitleEntry'.
app/lib/map/editor/duchyAssignment.test.ts(41,56): error TS2345: Argument of type '{ DUCHY_1: { name: string; titles: string[]; }; DUCHY_2: { name: string; titles: string[]; }; }' is not assignable to parameter of type 'TitleDraft'.
  Property 'DUCHY_1' is incompatible with index signature.
    Property 'rgb' is missing in type '{ name: string; titles: string[]; }' but required in type 'EditorTitleEntry'.
app/lib/map/editor/paintTitleLayers.test.ts(185,20): error TS2339: Property 'data' does not exist on type 'never'.
app/lib/map/editor/paintTitleLayers.test.ts(186,20): error TS2339: Property 'data' does not exist on type 'never'.
app/lib/map/editor/paintTitleLayers.test.ts(187,20): error TS2339: Property 'data' does not exist on type 'never'.
app/lib/map/editor/paintTitleLayers.test.ts(188,20): error TS2339: Property 'data' does not exist on type 'never'.
app/lib/map/editor/paintTitleLayers.test.ts(215,20): error TS2339: Property 'data' does not exist on type 'never'.
app/lib/map/editor/paintTitleLayers.test.ts(216,20): error TS2339: Property 'data' does not exist on type 'never'.
app/lib/map/editor/paintTitleLayers.test.ts(217,20): error TS2339: Property 'data' does not exist on type 'never'.
app/lib/map/editor/paintTitleLayers.test.ts(218,20): error TS2339: Property 'data' does not exist on type 'never'.
app/lib/map/editor/paintTitleLayers.test.ts(219,20): error TS2339: Property 'data' does not exist on type 'never'.
app/lib/map/editor/paintTitleLayers.test.ts(246,20): error TS2339: Property 'data' does not exist on type 'never'.
app/lib/map/editor/paintTitleLayers.test.ts(247,20): error TS2339: Property 'data' does not exist on type 'never'.
app/lib/map/editor/paintTitleLayers.test.ts(248,20): error TS2339: Property 'data' does not exist on type 'never'.
app/lib/map/editor/paintTitleLayers.test.ts(249,20): error TS2339: Property 'data' does not exist on type 'never'.
app/lib/mapLabels.test.ts(853,39): error TS2353: Object literal may only specify known properties, and 'rgb' does not exist in type 'TitleEntity'.
app/lib/mapLabels.test.ts(854,46): error TS2353: Object literal may only specify known properties, and 'rgb' does not exist in type 'TitleEntity'.
lib/characters/loreSkinMode.test.ts(48,16): error TS2322: Type '{ existing_skin_id: string; }' is not assignable to type 'LoreItemDraft & Partial<LoreItemDraft>'.
  Type '{ existing_skin_id: string; }' is missing the following properties from type 'LoreItemDraft': display_name, lore, submission_id, submission_status
lib/characters/loreSkinMode.test.ts(64,11): error TS2322: Type '{ state: string; submission_id: string; }' is not assignable to type 'LoreItemDraft & Partial<LoreItemDraft>'.
  Type '{ state: string; submission_id: string; }' is missing the following properties from type 'LoreItemDraft': display_name, lore, existing_skin_id, submission_status
