# kingscripts Python Package

This open source python package allows for easy access to the majority of KOC data products for KOC employees. Currently on version 2.0.8

Developed and Maintained by Michael Tanner. Please email mtanner@kingoperating.com with any questions.

Visit [KOC Development Site](https://mtanner161.github.io/kingdashboard/#/kingdashboard) for our ongoing front-end application development

One moudle `enverus`

1.  `enverus.getWellProductionData` - returns pandas dataframe of monthly oil/gas/water production

- Arguments:
  - `apiKey`: Enverus API authentication `object`
  - `wellApi14`: Well API14 of interest `str`
