library(RODBC)
library(ggplot2)
library(reshape)


prod <- odbcConnect("TRA_Prod")
dev <- odbcConnect("TRA_Dev")

mikeFinelines <- sqlQuery(prod, "select 
                                  di.FINELINE_NO,
                                	di.FINELINE_DESCR,
                                	count(*) as rowCnt,
                                	sum(wtd.POS_QTY) posQty,
                                	sum(wtd.POS_SALES_AMT) posSales
                                from tra_stg_mss.landing.IMPORT_RETAILLINK_DAILY_STORE_ITEM_WTD_DAILY_COLUMNS wtd
                                inner join tra_mart_mss.dbo.dim_item di
                                	on wtd.item_no = di.item_no
                                	and di.ITEM_CURRENT_IND = 'Current'
                                group by 
                                	di.FINELINE_NO,
                                	di.FINELINE_DESCR
                                order by FINELINE_NO")

japrilFinelines <- sqlQuery(dev, "select 
                                  di.FINELINE_NO,
                                  di.FINELINE_DESCR,
                                	count(*) as rowCnt,
                                	sum(wtd.POS_QTY) posQty,
                                	sum(wtd.POS_SALES_AMT) posSales
                                from tra_stg_mss.landing.IMPORT_RETAILLINK_DAILY_STORE_ITEM_WTD_DAILY_COLUMNS wtd
                                inner join tra_mart_mss.dbo.dim_item di
                                	on wtd.item_no = di.item_no
                                	and di.ITEM_CURRENT_IND = 'Current'
                                group by 
                                	di.FINELINE_NO,
                                	di.FINELINE_DESCR
                                order by FINELINE_NO")
odbcClose(prod)
odbcClose(dev)


merged = merge(x=japrilFinelines, y=mikeFinelines, by="FINELINE_NO", all = TRUE)
merged$rowCntDiff = merged$rowCnt.y - merged$rowCnt.x

# Melt data turning column values into rows
meltedRowCnt= melt(merged[,c("FINELINE_NO", "rowCnt.x", "rowCnt.y")], id=c("FINELINE_NO"), variable_name="Source")
meltedPosQty= melt(merged[,c("FINELINE_NO", "posQty.x", "posQty.y")], id=c("FINELINE_NO"), variable_name="Source")

# Rename value identifiers to friendlier labels
levels(meltedRowCnt$RowCntSource) <- c("Aprilia", "Mike")

# Function to plot and save a fineline from a df
doPlot = function(fl, df) {
  dum = subset(df, FINELINE_NO == fl)
  ggobj = ggplot(data = dum, aes(x=RowCntSource, y=value)) + geom_bar(stat="identity", aes(fill=RowCntSource))
  ggobj = ggobj + ggtitle(sprintf("Row Counts for fineline: %s", fl))
  ggobj = ggobj + geom_text(aes(label = value, y = value-(value/2)))
  print(ggobj)
  ggsave(sprintf("%s.pdf", fl))
}

#doPlot(1, meltedRowCnt)
lapply(unique(meltedRowCnt$FINELINE_NO), doPlot, meltedRowCnt)

#g = ggplot(merged, aes(x=FINELINE_NO, y=rowCntDiff))
#g + geom_bar(stat="identity")
