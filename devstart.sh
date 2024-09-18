rm -rf build;
cd frontend; 
npm run build;
cp -r build ../;
cd -;
docker compose down;docker compose down --volumes; docker compose build;docker compose up;