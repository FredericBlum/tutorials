library(readr)
library(dplyr)
library(ggplot2)
library(rnaturalearth)
library(rnaturalearthdata)

###################################
languages <- read_csv('languages.tsv', na=c(''))
colors <- c('#0055ff', '#d24d00', '#ff69ca', '#0000ae', '#aeff0c', '#04594d', '#20d2ff',
            '#18a68e', '#590000', '#450059', '#c60065', '#ffaa96', '#ba10c2')
################################################
#####             Maps                     #####
################################################

spdf_sa <- ne_countries(continent=c("south america", 'north america'),
                        scale="medium", 
                        returnclass="sf")

rivers <- ne_download(scale = 50, type = 'rivers_lake_centerlines', category = 'physical', returnclass = "sf")


# Plotting the language points and labels on the map
map_lex <- ggplot(data=languages) +
  geom_sf(data = spdf_sa) +
  geom_sf(data = rivers) +
  coord_sf(ylim=c(-20, 40), xlim= c(-125, -35)) +
  geom_point(aes(x=longitude,y=latitude, fill=family), size=5, shape=21) +
  scale_fill_manual(values=colors) +
  theme_bw() +
  theme(legend.position="right",
        axis.title = element_text(size = rel(1.3)),
        axis.text = element_text(size = rel(1.3)),
        legend.text = element_text(size = rel(1.5)),
        legend.spacing.y = unit(0.5, 'cm'),
        legend.spacing.x = unit(0.2, 'cm'),
        legend.title = element_text(size = rel(0)))


map_lex
ggsave('map.png', map_lex, scale=1, width=3000, height=2000, units="px")
