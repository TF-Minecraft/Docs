> Canonical documentation: [TF-Minecraft/docs](https://github.com/TF-Minecraft/docs). [Source snapshot](https://github.com/TF-Minecraft/ProvinceSystem/blob/9b34fd3fd336af9025ca187ca9610690695c0efa/docs/wiki-research/validation/wiki-tests.txt). Commands and plain-text code/config paths refer to the source repository unless stated otherwise.


> servermap@0.1.0 test
> vitest run


 RUN  v3.2.7 C:/Users/MSI/Desktop/ProvinceSystem/frontend

 ❯ app/lib/titleProvinces.test.ts (8 tests | 1 failed) 13ms
   ✓ resolveTitleProvinces > returns county provinces directly 1ms
   ✓ resolveTitleProvinces > rolls up duchy through counties 0ms
   ✓ resolveTitleProvinces > rolls up kingdom through duchy 0ms
   ✓ resolveTitleProvinces > rolls up empire through kingdom with no duplicates 0ms
   ✓ resolveTitleProvinces > falls through kingdom child to county when not in duchy layer 0ms
   ✓ resolveTitleProvinces > unions direct provinces and nested titles on incomplete holders 0ms
   ✓ resolveTitleProvinces > returns trade guild provinces 0ms
   × KINGDOM_1 spot-check (main defines) > matches union of COUNTY_1 through COUNTY_9 provinces 10ms
     → expected [ Array(80) ] to deeply equal [ Array(47) ]
 ✓ app/lib/precedent/playerSuggest.test.ts (16 tests) 25ms
 ✓ app/lib/map/chronicleStaff.test.ts (38 tests) 45ms
 ✓ app/lib/map/gif/encodeGif.test.ts (13 tests) 86ms
 ✓ app/lib/mapLabels.test.ts (51 tests) 28ms
 ✓ app/lib/map/gif/gifPalette.test.ts (10 tests) 149ms
 ✓ app/lib/map/ledgerSeries.test.ts (85 tests) 181ms
 ✓ app/hooks/useEditorProvinceIndex.test.ts (14 tests) 115ms
 ✓ app/lib/map/dataSource.test.ts (23 tests) 61ms
 ✓ app/lib/map/chronicleData.test.ts (9 tests) 308ms
 ✓ app/lib/map/chronicleTradeLeagues.test.ts (6 tests) 26ms
 ✓ app/lib/labelBlobGeometry.test.ts (24 tests) 34ms
 ✓ app/lib/map/chronicleFocus.test.ts (15 tests) 25ms
 ✓ app/lib/map/api.test.ts (8 tests) 22ms
 ✓ app/lib/map/ledgerData.test.ts (14 tests) 16ms
 ✓ app/lib/map/chronicleOwnership.test.ts (16 tests) 15ms
 ✓ app/lib/mapPaintGeometry.test.ts (51 tests) 19ms
 ✓ app/lib/map/chronicleGifFrame.test.ts (33 tests) 16ms
 ✓ app/lib/map/chronicleBuild.test.ts (30 tests) 19ms
 ✓ app/components/chronicle/chronicleLayers.test.ts (36 tests) 17ms
 ✓ app/lib/warCampaignLine.test.ts (20 tests) 15ms
 ✓ app/lib/mapPaintStorage.test.ts (16 tests) 15ms
 ✓ app/lib/precedent/filter.test.ts (29 tests) 17ms
 ✓ app/lib/map/editorAccess.test.ts (6 tests) 20ms
 ✓ app/lib/mapPaint.test.ts (29 tests) 12ms
 ✓ app/lib/map/chronicleDayRoute.test.ts (24 tests) 12ms
 ✓ app/lib/map/chronicleFillStack.test.ts (19 tests) 10ms
 ✓ app/lib/map/editor/buildEditorTitlesZip.test.ts (3 tests) 12ms
 ✓ app/wiki/data/registry.test.ts (16 tests) 51ms
 ✓ app/lib/map/chroniclePaint.test.ts (15 tests) 13ms
 ✓ app/lib/map/chronicleBorderMask.test.ts (12 tests) 12ms
 ✓ app/lib/map/chronicleProsperity.test.ts (17 tests) 11ms
 ✓ app/lib/mapMarkers.test.ts (15 tests) 10ms
 ✓ app/lib/map/chronicleOccupation.test.ts (14 tests) 11ms
 ✓ app/lib/map/chronicleDayModes.test.ts (11 tests) 9ms
 ✓ app/lib/map/editor/provinceRunIndex.test.ts (341 tests) 1566ms
   ✓ real main artifacts: runs decode to the same grid > matches province_id_grid.bin.gz pixel for pixel  306ms
   ✓ real main artifacts: runs decode to the same grid > has a bbox row for exactly the province ids present in the grid  747ms
 ✓ app/lib/map/chronicleFortControl.test.ts (11 tests) 9ms
 ✓ app/lib/warBattleMarkers.test.ts (11 tests) 10ms
 ✓ app/lib/map/editor/paintTitleLayers.test.ts (10 tests) 10ms
 ✓ app/lib/map/editor/validateEditorDraft.test.ts (9 tests) 12ms
 ✓ app/core/mapObjectBuilder.test.ts (12 tests) 8ms
 ✓ app/lib/mapViewportMath.test.ts (18 tests) 10ms
 ✓ app/wiki/vehicles/vehicles.test.ts (6 tests) 561ms
 ✓ app/lib/site/staffAccess.test.ts (5 tests) 10ms
 ✓ app/lib/map/editor/buildProvinceIndex.test.ts (5 tests) 7ms
 ✓ app/lib/map/chronicleInfestation.test.ts (12 tests) 8ms
 ✓ app/lib/mapPaintHistory.test.ts (7 tests) 7ms
 ✓ app/lib/settlementMarkers.test.ts (6 tests) 8ms
 ✓ app/hooks/useProvinceHover.test.ts (10 tests) 7ms
 ✓ app/hooks/useMapCoords.test.ts (10 tests) 8ms
 ✓ app/components/chronicle/chronicleGifExport.test.ts (2 tests) 6ms
 ✓ app/lib/map/editor/editorLoadProgress.test.ts (6 tests) 8ms
 ✓ app/lib/map/titleRgb.test.ts (6 tests) 7ms
 ✓ app/lib/map/editor/countyAssignment.test.ts (6 tests) 5ms
 ✓ app/lib/map/editor/childTitleDraftActions.test.ts (3 tests) 6ms
 ✓ app/lib/installationMarkers.test.ts (2 tests) 5ms
 ✓ app/lib/map/editor/duchyDraftActions.test.ts (3 tests) 5ms
 ✓ app/lib/map/editor/countyDraftActions.test.ts (4 tests) 6ms
 ✓ app/lib/map/editor/childTitleAssignment.test.ts (4 tests) 6ms
 ✓ app/lib/map/editor/validateAllTiersForExport.test.ts (4 tests) 5ms
 ✓ app/lib/map/provinceCounty.test.ts (5 tests) 5ms
 ✓ app/lib/fortZoc.test.ts (6 tests) 5ms
 ✓ app/lib/map/editor/duchyAssignment.test.ts (4 tests) 5ms
 ✓ app/lib/map/gif/gifLzw.test.ts (10 tests) 3360ms
   ✓ lzwCompress > round-trips a run long enough to fill and reset the code table  1592ms
   ✓ lzwCompress > round-trips a long run of blocks that each fill the table  1161ms
 ✓ app/hooks/regionPick.test.ts (4 tests) 6ms
 ✓ app/lib/map/editorParams.test.ts (5 tests) 5ms
 ✓ lib/characters/loreSkinMode.test.ts (4 tests) 4ms
 ✓ app/lib/map/editor/buildCountyPickIndex.test.ts (2 tests) 4ms
 ✓ app/lib/map/editor/buildTitlePickIndex.test.ts (2 tests) 4ms
 ✓ app/hooks/useMapViewport.test.ts (1 test) 4ms
 ✓ app/wiki/wikiRoutes.test.tsx (48 tests) 671ms
 ✓ app/components/chronicle/chronicleGifExportChunking.test.ts (7 tests) 114ms
 ✓ app/components/chronicle/ChroniclePanels.test.tsx (6 tests) 61ms
 ✓ app/components/chronicle/ChronicleStaffConsole.test.tsx (3 tests) 112ms
 ✓ app/components/chronicle/LedgerChartsPanel.test.tsx (5 tests) 202ms
node.exe : stderr | app/components/chronicle/ChronicleStudio.test.tsx > ChronicleStudio > mounts and paints its first s
tep
At line:1 char:1
+ & "C:\Program Files\nodejs/node.exe" "C:\Users\MSI\AppData\Roaming\np ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (stderr | app/co... its first step:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
Not implemented: HTMLCanvasElement's getContext() method: without installing the canvas npm package
Not implemented: HTMLCanvasElement's getContext() method: without installing the canvas npm package

 ✓ app/components/chronicle/ChronicleStudio.test.tsx (2 tests) 117ms
 ✓ app/components/chronicle/ChronicleOwnershipLayer.test.tsx (3 tests) 62ms
 ✓ app/components/wiki/wikiComponents.test.tsx (15 tests) 220ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  app/lib/titleProvinces.test.ts > KINGDOM_1 spot-check (main defines) > matches union of COUNTY_1 through COUNTY_
9 provinces
AssertionError: expected [ Array(80) ] to deeply equal [ Array(47) ]

- Expected
+ Received

@@ -13,10 +13,12 @@
    12,
    13,
    14,
    15,
    16,
+   17,
+   18,
    19,
    20,
    21,
    22,
    23,
@@ -27,23 +29,54 @@
    28,
    29,
    30,
    31,
    32,
+   33,
+   34,
    35,
    36,
    37,
    38,
    39,
    136,
    138,
    139,
    170,
+   171,
+   172,
+   173,
+   174,
+   175,
+   176,
+   177,
+   178,
+   179,
+   180,
+   181,
+   182,
+   183,
+   184,
+   185,
+   186,
+   187,
+   188,
+   189,
+   190,
+   191,
+   192,
+   193,
+   194,
+   195,
+   196,
+   197,
+   198,
    397,
    398,
    399,
    400,
    401,
    402,
    403,
    741,
+   742,
  ]

 ❯ app/lib/titleProvinces.test.ts:117:42
    115| 
    116|     const result = resolveTitleProvinces("KINGDOM_1", "kingdom", layer…
    117|     expect(result.sort((a, b) => a - b)).toEqual(
       |                                          ^
    118|       [...new Set(expected)].sort((a, b) => a - b)
    119|     );

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/1]⎯


 Test Files  1 failed | 77 passed (78)
      Tests  1 failed | 1390 passed (1391)
   Start at  16:32:20
   Duration  9.47s (transform 9.03s, setup 0ms, collect 23.85s, tests 8.71s, environment 24.28s, prepare 15.02s)

