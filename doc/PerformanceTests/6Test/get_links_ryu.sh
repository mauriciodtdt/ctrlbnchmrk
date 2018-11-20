echo "links"
curl -X GET http://10.0.1.10:8080/v1.0/topology/links | tr '{' '\n' | grep src | wc -l
echo ""
echo "switches"
curl -X GET http://10.0.1.10:8080/stats/switches | awk -F' ' '{print NF; exit}'
